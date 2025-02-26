"""ESMFold implementation for protein structure prediction using Meta AI's ESM-2 model."""

import logging
from dataclasses import dataclass
from typing import Optional, List, Union

import modal
import numpy as np

from . import app
from .base import FoldingAlgorithm, StructurePrediction, PredictionMetadata
from .images.esmfold import esmfold_image
from .images.volumes import model_weights
from .utils import MINUTES, MODEL_DIR
from .utils import Timer

# Set up basic logging configuration
logging.basicConfig(level=logging.INFO)


@dataclass
class ESMFoldOutput(StructurePrediction):
    """Output from ESMFold prediction including all model outputs."""

    # TODO: we should figure out what should be the verbosity of the output,
    # as a usual user does not need all of this information

    # Required by StructurePrediction protocol
    positions: np.ndarray  # (model_layer, batch_size, residue, atom=14, xyz=3)
    metadata: PredictionMetadata

    # Additional ESMFold-specific outputs
    frames: np.ndarray  # (model_layer, batch_size, residue, qxyz=7)
    sidechain_frames: np.ndarray  # (model_layer, batch_size, residue, ?, 4, 4) ??
    unnormalized_angles: np.ndarray  # (model_layer, batch_size, residue, 7, 2) ??
    angles: np.ndarray  # (model_layer, batch_size, residue, 7, 2) ??
    states: np.ndarray  # (model_layer, batch_size, residue, ???)
    s_s: np.ndarray  # (batch_size, residue, 1024)
    s_z: np.ndarray  # (batch_size, residue, residue, 128)
    distogram_logits: np.ndarray  # (batch_size, residue, residue, 64) ???
    lm_logits: np.ndarray  # (batch_size, residue, 23) ???
    aatype: np.ndarray  # (batch_size, residue) amino acid identity
    atom14_atom_exists: np.ndarray  # (batch_size, residue, atom=14)
    residx_atom14_to_atom37: np.ndarray  # (batch_size, residue, atom=14)
    residx_atom37_to_atom14: np.ndarray  # (batch_size, residue, atom=37)
    atom37_atom_exists: np.ndarray  # (batch_size, residue, atom=37)
    residue_index: np.ndarray  # (batch_size, residue)
    lddt_head: np.ndarray  # (model_layer, batch_size, residue, atom=37, 50) ??
    plddt: np.ndarray  # (batch_size, residue, residue, atom=37)
    ptm_logits: np.ndarray  # (batch_size, residue, residue, 64) ???
    ptm: np.ndarray  # float # TODO: make it into a float when sending to the client
    aligned_confidence_probs: np.ndarray  # (batch_size, residue, residue, 64)
    predicted_aligned_error: np.ndarray  # (batch_size, residue, residue)
    max_predicted_aligned_error: np.ndarray  # float # TODO: make it into a float when sending to the client
    chain_index: np.ndarray  # (batch_size, residue)
    pdb: Optional[list[str]] = None
    cif: Optional[list[str]] = None

    # TODO: can add a save method here (to a pickle and a pdb file) that can be run locally


with esmfold_image.imports():
    import torch
    from transformers import EsmForProteinFolding, AutoTokenizer


@app.cls(
    image=esmfold_image,
    gpu="T4",
    timeout=20 * MINUTES,
    container_idle_timeout=10 * MINUTES,
    volumes={MODEL_DIR: model_weights},
)
class ESMFold(FoldingAlgorithm):
    """ESMFold protein structure prediction model."""

    # TODO: maybe this config should be input to the fold function, so that it can
    # changed programmatically on a single ephermal app, rather than re-creating the app?
    DEFAULT_CONFIG = {
        # ESMFold model config
        "output_pdb": False,
        "output_cif": False,
        # Chain linking and positioning config
        "glycine_linker": "G" * 50,
        "position_ids_skip": 512,
    }

    # We need to properly asses whether using this or the original ESMFold is better
    # based on speed, accuracy, bugs, etc.; as well as customizability
    # For instance, if we want to also allow differently sized structure modules, than this would be good
    # TODO: we should add a settings dictionary or something, that would make it easier to add new options
    # TODO: maybe use OmegaConf instead to make it easier instead of config
    def __init__(self, config: dict = {}) -> None:
        """Initialize ESMFold."""
        super().__init__()
        self.config = {**self.DEFAULT_CONFIG, **config}
        self.metadata = self._initialize_metadata(
            model_name="ESMFold",
            model_version="v4.49.0",  # HuggingFace transformers version
        )

        self._linker_map: Optional[torch.Tensor] = None

    @modal.enter()
    def _load(self) -> None:
        """Load the ESMFold model and tokenizer."""
        self.tokenizer: AutoTokenizer = AutoTokenizer.from_pretrained("facebook/esmfold_v1", cache_dir=MODEL_DIR)
        self.model: EsmForProteinFolding = EsmForProteinFolding.from_pretrained(
            "facebook/esmfold_v1", cache_dir=MODEL_DIR
        )
        self.device = "cuda"
        self.model = self.model.cuda()
        self.model.eval()
        self.model.trunk.set_chunk_size(64)
        self.ready = True

    @modal.method()
    def fold(self, sequences: Union[str, List[str]]) -> ESMFoldOutput:
        """Predict protein structure(s) using ESMFold."""
        if not hasattr(self, "tokenizer"):
            raise RuntimeError("Model not loaded. Call _load() first.")
        if not hasattr(self, "model"):
            raise RuntimeError("Model not loaded. Call _load() first.")

        if isinstance(sequences, str):
            sequences = [sequences]

        sequences = self._validate_sequences(sequences)
        self.metadata.sequence_lengths = self._compute_sequence_lengths(sequences)

        tokenized_input = self._tokenize_sequences(sequences)

        with Timer("Model Inference") as timer:
            with torch.inference_mode():
                outputs = self.model(**tokenized_input)

        outputs = self._convert_outputs(outputs, timer.duration)
        return outputs

    def _tokenize_sequences(self, sequences: List[str]) -> torch.Tensor:
        if ":" in "".join(sequences):  # MULTIMER setting
            tokenized = self._tokenize_multimer(sequences)
        else:  # MONOMER setting
            tokenized = self.tokenizer(
                sequences, return_tensors="pt", add_special_tokens=False, padding=True, truncation=True, max_length=1024
            )
        tokenized = {k: v.to(self.device) for k, v in tokenized.items()}

        return tokenized

    @staticmethod
    def _compute_position_ids(_sequences: List[str], glycine_linker: str, position_ids_skip: int) -> torch.Tensor:
        position_ids = []
        for multimer_seq in _sequences:  # for every sequence in the batch
            # TODO: Should position_ids start with 0 or 1?
            # Stefano worked with 0, as that is what was used Meta's original implementation
            # Does it even matter though?
            multimer_position_ids = []
            previous_chain_end = 0
            for chain_id, chain_seq in enumerate(multimer_seq.split(":")):
                intrachain_position_ids = np.arange(len(chain_seq))
                if chain_id != 0:
                    intrachain_position_ids = (intrachain_position_ids + (previous_chain_end + 1)) + position_ids_skip

                # add linker if not last chain
                if chain_id != len(multimer_seq.split(":")) - 1:
                    linker_position_ids = np.arange(len(glycine_linker)) + intrachain_position_ids[-1] + 1
                    intrachain_position_ids = np.concatenate([intrachain_position_ids, linker_position_ids])

                previous_chain_end = intrachain_position_ids[-1]
                multimer_position_ids += intrachain_position_ids.tolist()
            position_ids.append(torch.tensor(multimer_position_ids))

        # add padding to the position ids
        max_length = max(len(ids) for ids in position_ids)
        for i, pos_ids in enumerate(position_ids):
            position_ids[i] = torch.cat([pos_ids, torch.zeros(max_length - len(pos_ids), dtype=torch.long)])
            # TODO: adding ZEROs might not be the best idea, but it works for now
        return torch.stack(position_ids)

    @staticmethod
    def _store_multimer_properties(
        _sequences: List[str], glycine_linker: str
    ) -> tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
        """Store properties needed for multimer processing.

        Args:
            _sequences: List of sequences, each containing chains separated by ":"
            glycine_linker: The glycine linker string used between chains

        Returns:
            tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
                - linker_map: tensor of shape (batch_size, sequence_length) where 1 indicates
                linker positions and 0 indicates chain positions
                - residue_index: tensor of shape (batch_size, sequence_length) containing
                residue indices that restart at 1 for each chain
                - chain_index: tensor of shape (batch_size, sequence_length) containing
                chain indices (0, 1, 2, etc.)
        """
        linker_map = []
        residue_index = []
        chain_index = []

        assert len(_sequences) > 0, "Sequences must not be empty"

        for seq in _sequences:
            # Initialize masks for the full sequence
            full_seq_len = len(seq.replace(":", glycine_linker))
            seq_mask = torch.zeros(full_seq_len, dtype=torch.long)
            res_index = torch.zeros(full_seq_len, dtype=torch.long)
            ch_index = torch.zeros(full_seq_len, dtype=torch.long)

            # Process each chain
            current_pos = 0
            chains = seq.split(":")

            for i, chain in enumerate(chains):
                # Set chain index for current chain
                ch_index[current_pos : current_pos + len(chain)] = i

                # Set residue indices for current chain (1-based indexing)
                res_index[current_pos : current_pos + len(chain)] = torch.arange(1, len(chain) + 1)

                current_pos += len(chain)

                # Add linker properties if not the last chain
                if i < len(chains) - 1:
                    # Mark linker positions
                    seq_mask[current_pos : current_pos + len(glycine_linker)] = 1
                    # Set chain index for linker (same as previous chain)
                    ch_index[current_pos : current_pos + len(glycine_linker)] = i
                    # Set residue indices for linker (continuing from previous chain)
                    res_index[current_pos : current_pos + len(glycine_linker)] = torch.arange(
                        len(chain) + 1, len(chain) + len(glycine_linker) + 1
                    )
                    current_pos += len(glycine_linker)

            linker_map.append(seq_mask)
            residue_index.append(res_index)
            chain_index.append(ch_index)

        return torch.stack(linker_map), torch.stack(residue_index), torch.stack(chain_index)

    @staticmethod
    def _replace_glycine_linkers(_sequences: List[str], glycine_linker: str) -> List[str]:
        for i, multimer_seq in enumerate(_sequences):
            _sequences[i] = multimer_seq.replace(":", glycine_linker)  # replace : with glycine linkers
        return _sequences

    def _tokenize_multimer(self, sequences: List[str]) -> torch.Tensor:
        self._linker_map, self._residue_index, self.chain_index = self._store_multimer_properties(
            sequences, self.config["glycine_linker"]
        )
        _sequences = self._replace_glycine_linkers(sequences, self.config["glycine_linker"]).copy()
        tokenized = self.tokenizer(_sequences, return_tensors="pt", add_special_tokens=False)
        tokenized["position_ids"] = self._compute_position_ids(
            _sequences, self.config["glycine_linker"], self.config["position_ids_skip"]
        )
        return tokenized

    def _mask_linker_region(self, outputs: dict) -> dict:
        """Mask the linker region in the outputs.
        This includes all the metrics.

        Args:
            outputs: Dictionary containing model outputs
            sequences: List of input sequences

        Returns:
            dict: Updated outputs with linker regions masked
        """
        # Invert the linker map (0->1, 1->0)
        assert isinstance(self._linker_map, torch.Tensor), "linker_map must be a tensor"
        mask = 1 - self._linker_map.unsqueeze(-1)

        outputs["chain_index"] = self.chain_index.cpu().numpy()

        # TODO: someone has to check the batching as I believe this will not work!!!
        for multimer in mask:
            chain_indices = np.nonzero(multimer.squeeze(-1).cpu().numpy())[0].tolist()
            outputs["positions"] = outputs["positions"][
                :, :, chain_indices
            ]  # 3rd dim is residue index (for others, it differs)
            outputs["frames"] = outputs["frames"][:, :, chain_indices]
            outputs["sidechain_frames"] = outputs["sidechain_frames"][:, :, chain_indices]
            outputs["unnormalized_angles"] = outputs["unnormalized_angles"][:, :, chain_indices]
            outputs["angles"] = outputs["angles"][:, :, chain_indices]
            outputs["states"] = outputs["states"][:, :, chain_indices]
            outputs["s_s"] = outputs["s_s"][:, chain_indices]
            outputs["s_z"] = outputs["s_z"][:, chain_indices]
            outputs["distogram_logits"] = outputs["distogram_logits"][:, chain_indices]
            outputs["lm_logits"] = outputs["lm_logits"][:, chain_indices]
            outputs["aatype"] = outputs["aatype"][:, chain_indices]
            outputs["atom14_atom_exists"] = outputs["atom14_atom_exists"][:, chain_indices]
            outputs["residx_atom14_to_atom37"] = outputs["residx_atom14_to_atom37"][:, chain_indices]
            outputs["residx_atom37_to_atom14"] = outputs["residx_atom37_to_atom14"][:, chain_indices]
            outputs["atom37_atom_exists"] = outputs["atom37_atom_exists"][:, chain_indices]
            outputs["residue_index"] = self._residue_index[:, chain_indices].cpu().numpy()  # custom residue indices
            outputs["lddt_head"] = outputs["lddt_head"][:, :, chain_indices]
            outputs["plddt"] = outputs["plddt"][:, chain_indices]
            outputs["ptm_logits"] = outputs["ptm_logits"][:, chain_indices, chain_indices]
            outputs["aligned_confidence_probs"] = outputs["aligned_confidence_probs"][:, chain_indices, chain_indices]
            outputs["predicted_aligned_error"] = outputs["predicted_aligned_error"][:, chain_indices, chain_indices]
            outputs["chain_index"] = outputs["chain_index"][:, chain_indices]

        return outputs

    def _convert_outputs(self, outputs: dict, prediction_time: float) -> ESMFoldOutput:
        """Convert model outputs to ESMFoldOutput format."""

        outputs = {k: v.cpu().numpy() for k, v in outputs.items()}
        if self._linker_map is not None:
            # TODO: maybe add a proper MULTIMER flag?
            outputs = self._mask_linker_region(outputs)
        else:
            outputs["chain_index"] = np.zeros(outputs["residue_index"].shape, dtype=np.int32)

        self.metadata.prediction_time = prediction_time

        if self.config["output_pdb"]:
            outputs["pdb"] = self._convert_outputs_to_pdb(outputs)
        if self.config["output_cif"]:
            outputs["cif"] = self._convert_outputs_to_cif(outputs)

        return ESMFoldOutput(metadata=self.metadata, **outputs)

    def _convert_outputs_to_pdb(self, outputs: dict) -> list[str]:
        from transformers.models.esm.openfold_utils.protein import to_pdb, Protein as OFProtein
        from transformers.models.esm.openfold_utils.feats import atom14_to_atom37

        final_atom_positions = atom14_to_atom37(outputs["positions"][-1], outputs)
        final_atom_mask = outputs["atom37_atom_exists"]
        pdbs = []

        for i in range(outputs["aatype"].shape[0]):
            aa = outputs["aatype"][i]
            pred_pos = final_atom_positions[i]
            mask = final_atom_mask[i]
            resid = outputs["residue_index"][i] + 1
            pred = OFProtein(
                aatype=aa,
                atom_positions=pred_pos,
                atom_mask=mask,
                residue_index=resid,
                b_factors=outputs["plddt"][i],
                chain_index=outputs["chain_index"][i] if "chain_index" in outputs else None,
            )
            pdbs.append(to_pdb(pred))

        return pdbs

    def _convert_outputs_to_cif(self, outputs: dict) -> list[str]:
        raise NotImplementedError("CIF conversion not implemented yet")
        from transformers.models.esm.openfold_utils.protein import to_modelcif, Protein as OFProtein
        from transformers.models.esm.openfold_utils.feats import atom14_to_atom37

        final_atom_positions = atom14_to_atom37(outputs["positions"][-1], outputs)
        final_atom_mask = outputs["atom37_atom_exists"]
        cifs = []
        for i in range(outputs["aatype"].shape[0]):
            aa = outputs["aatype"][i]
            pred_pos = final_atom_positions[i]
            mask = final_atom_mask[i]
            resid = outputs["residue_index"][i] + 1
            pred = OFProtein(
                aatype=aa,
                atom_positions=pred_pos,
                atom_mask=mask,
                residue_index=resid,
                b_factors=outputs["plddt"][i],
                chain_index=outputs["chain_index"][i] if "chain_index" in outputs else None,
            )
            cifs.append(to_modelcif(pred))

        return cifs
