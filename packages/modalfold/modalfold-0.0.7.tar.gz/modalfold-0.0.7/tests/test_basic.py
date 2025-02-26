"""Test suite for ModalFold package."""

from typing import Generator

import numpy as np
import pytest
import torch
from modal import enable_output

from modalfold import app
from modalfold.esmfold import ESMFold, ESMFoldOutput
from modalfold.utils import validate_sequence, format_time

# Test sequences
TEST_SEQUENCES = {
    "short": "MLKNVHVLVLGAGDVGSVVVRLLEK",  # 24 residues
    "medium": "MALWMRLLPLLALLALWGPDPAAAFVNQHLCGSHLVEALYLVCGERGFFYTPKT",  # Insulin
    "invalid": "MALWMRLLPX123LLALWGPD",  # Contains invalid characters
    "multimer": "MALWMRLLPLLALLALWGPDPAAAFVNQHLCGSHLVEALYLVCGERGFFYTPKT:MALWMRLLPLLALLALWGPDPAAAFVNQHLCGSHLVEALYLVCGERGFFYTPKT",  # 2x Insulin
}


@pytest.fixture
def esmfold_model() -> Generator[ESMFold, None, None]:
    """Fixture for ESMFold model."""
    with enable_output():
        with app.run():
            model = ESMFold()
            yield model


def test_validate_sequence():
    """Test sequence validation."""
    # Valid sequences
    assert validate_sequence(TEST_SEQUENCES["short"]) is True
    assert validate_sequence(TEST_SEQUENCES["medium"]) is True

    # Invalid sequences
    with pytest.raises(ValueError):
        validate_sequence(TEST_SEQUENCES["invalid"])
    with pytest.raises(ValueError):
        validate_sequence("NOT A SEQUENCE")


def test_format_time():
    """Test time formatting."""
    assert format_time(30) == "30s", f"Expected '30s', got {format_time(30)}"
    assert format_time(90) == "1m 30s", f"Expected '1m 30s', got {format_time(90)}"
    assert format_time(3600) == "1h", f"Expected '1h', got {format_time(3600)}"
    assert format_time(3661) == "1h 1m 1s", f"Expected '1h 1m 1s', got {format_time(3661)}"


def test_esmfold_basic():
    """Test basic ESMFold functionality."""

    with enable_output():
        with app.run():
            model = ESMFold()
            result = model.fold.remote(TEST_SEQUENCES["short"])

            assert isinstance(result, ESMFoldOutput), "Result should be an ESMFoldOutput"

            seq_len = len(TEST_SEQUENCES["short"])
            positions_shape = result.positions.shape

            assert positions_shape[-1] == 3, "Coordinate dimension mismatch. Expected: 3, Got: {positions_shape[-1]}"
            assert (
                positions_shape[-3] == seq_len
            ), "Number of residues mismatch. Expected: {seq_len}, Got: {positions_shape[-3]}"
            assert np.all(result.plddt >= 0), "pLDDT scores should be non-negative"
            assert np.all(result.plddt <= 100), "pLDDT scores should be less than or equal to 100"


def test_esmfold_multimer():
    """Test ESMFold multimer functionality."""
    with enable_output():
        with app.run():
            model = ESMFold(config={"output_pdb": True})
            result = model.fold.remote(TEST_SEQUENCES["multimer"])

    assert result.pdb is not None, "PDB output should be generated"
    assert result.positions.shape[2] == len(TEST_SEQUENCES["multimer"].replace(":", "")), "Number of residues mismatch"
    assert np.all(result.residue_index[0][:54] == np.arange(1, 55)), "First chain residue index mismatch"
    assert np.all(result.residue_index[0][54:] == np.arange(1, 55)), "Second chain residue index mismatch"
    assert np.all(result.chain_index[0][:54] == 0), "First chain index mismatch"
    assert np.all(result.chain_index[0][54:] == 1), "Second chain index mismatch"

    from modalfold.convert import pdb_string_to_atomarray

    structure = pdb_string_to_atomarray(result.pdb[0])

    n_residues = len(set((chain, res) for chain, res in zip(structure.chain_id, structure.res_id)))

    assert n_residues == len(TEST_SEQUENCES["multimer"].replace(":", "")), "Number of residues mismatch"
    assert len(result.chain_index[0]) == n_residues, "Chain index length mismatch"
    assert len(result.residue_index[0]) == n_residues, "Residue index length mismatch"

    # Check chain assignments
    unique_chains = np.unique(structure.chain_id)
    assert len(unique_chains) == 2, f"Expected 2 chains, got {len(unique_chains)}"

    # Check residues per chain
    chain_a_residues = len(np.unique(structure.res_id[structure.chain_id == "A"]))
    chain_b_residues = len(np.unique(structure.res_id[structure.chain_id == "B"]))
    assert chain_a_residues == 54, f"Chain A should have 54 residues, got {chain_a_residues}"
    assert chain_b_residues == 54, f"Chain B should have 54 residues, got {chain_b_residues}"


def test_esmfold_linker_map():
    """Test ESMFold linker map."""
    sequences = ["AAAAAA:BBBBBBBBB", "CCCCC:DDDDDDD:EEEEEEE", "HHHH"]
    GLYCINE_LINKER = "G" * 50
    N = len(GLYCINE_LINKER)
    linker_map, _, _ = ESMFold._store_multimer_properties([sequences[0]], GLYCINE_LINKER)
    gt_map = torch.tensor([0] * 6 + [1] * N + [0] * 9)
    assert torch.all(linker_map == gt_map), "Linker map mismatch"

    linker_map, _, _ = ESMFold._store_multimer_properties([sequences[1]], GLYCINE_LINKER)
    gt_map = torch.tensor([0] * 5 + [1] * N + [0] * 7 + [1] * N + [0] * 7)
    assert torch.all(linker_map == gt_map), "Linker map mismatch"

    linker_map, _, _ = ESMFold._store_multimer_properties([sequences[2]], GLYCINE_LINKER)
    gt_map = torch.tensor([0] * 4)
    assert torch.all(linker_map == gt_map), "Linker map mismatch"


def test_esmfold_no_glycine_linker():
    """Test ESMFold no glycine linker."""
    model = ESMFold(
        config={
            "glycine_linker": "",
        }
    )

    with enable_output():
        with app.run():
            result = model.fold.remote(TEST_SEQUENCES["multimer"])

    assert result.positions is not None, "Positions should be generated"
    assert result.positions.shape[2] == len(TEST_SEQUENCES["multimer"].replace(":", "")), "Number of residues mismatch"

    assert result.residue_index is not None, "Residue index should be generated"
    assert result.plddt is not None, "pLDDT should be generated"
    assert result.ptm is not None, "pTM should be generated"

    # assert correct chain_indices
    assert np.all(result.chain_index[0] == np.array([0] * 54 + [1] * 54)), "Chain indices mismatch"
    assert np.all(
        result.residue_index[0] == np.concatenate([np.arange(1, 55), np.arange(1, 55)])
    ), "Residue index mismatch"


def test_esmfold_chain_indices():
    """
    Test ESMFold chain indices. Note that this is before we slice the linker out, that
    is why we need to check the presence of the linker indices here as well. And by construction,
    it is assigned to the first chain, i.e. 0.
    """
    sequences = ["AAAAAA:CCCCCCCCC", "CCCCC:DDDDDDD:EEEEEEE", "HHHH"]
    GLYCINE_LINKER = "G" * 50
    N = len(GLYCINE_LINKER)

    _, _, chain_indices = ESMFold._store_multimer_properties([sequences[0]], GLYCINE_LINKER)

    expected_chain_indices = np.concatenate(
        [
            np.zeros(6),  # First chain (6 residues)
            np.zeros(N),  # Linker region (N residues) - belongs to first chain
            np.ones(9),  # Second chain (9 residues)
        ]
    )
    assert np.array_equal(chain_indices[0], expected_chain_indices), "Chain indices mismatch"


def test_compute_position_ids_batch():
    """Test position IDs computation with batch processing."""
    sequences = ["AAAAAA:CCCCCCCCC", "CCCCC:DDDDDDD:EEEEEEE", "HHHH"]

    GLYCINE_LINKER = "G" * 50
    POSITION_IDS_SKIP = 512

    position_ids = ESMFold._compute_position_ids([sequences[0]], GLYCINE_LINKER, POSITION_IDS_SKIP)

    # Check first sequence (AAAAAA:CCCCCCCCC)
    seq1_ids = position_ids[0]
    assert position_ids.shape[0] == 1, "Batch size should be 1"
    assert torch.all(seq1_ids[: 6 + 50] == torch.arange(6 + 50)), "First chain + linker positions incorrect"
    assert torch.all(
        seq1_ids[6 + 50 :] == torch.arange(1 + 512 + 55, 1 + 512 + 55 + 9)
    ), "Second chain positions incorrect"

    # Check second sequence (CCCCC:DDDDDDD:EEEEEEE)
    position_ids = ESMFold._compute_position_ids([sequences[1]], GLYCINE_LINKER, POSITION_IDS_SKIP)
    seq2_ids = position_ids[0]

    assert torch.all(seq2_ids[:55] == torch.arange(55)), "First chain + linker positions incorrect"
    assert torch.all(seq2_ids[55:112] == torch.arange(567, 624)), "Second chain + linker positions incorrect"
    assert torch.all(seq2_ids[112:] == torch.arange(1136, 1143)), "Third chain positions incorrect"

    # Check third sequence (HHHH), do entire batch, but only check the third sequence
    position_ids = ESMFold._compute_position_ids(sequences, GLYCINE_LINKER, POSITION_IDS_SKIP)
    assert position_ids.shape[0] == 3, "Batch size should be 3"

    seq3_ids = position_ids[2]

    assert torch.all(seq3_ids[:4] == torch.arange(4)), "First chain positions incorrect"
    # Check its padding is all zeros
    assert torch.all(seq3_ids[4:] == torch.zeros(len(seq3_ids) - 4)), "Padding should be all zeros"

    # length of it should be 19 + 100, i.e. the longest sequence + 2 glycine linkers, which is the second sequence
    assert len(seq3_ids) == 19 + 100, "Length of sequence 3 should be 19 + 100"


def test_esmfold_batch(esmfold_model: ESMFold):
    """Test ESMFold batch prediction."""

    # Define input sequences
    sequences = [TEST_SEQUENCES["short"], TEST_SEQUENCES["medium"]]

    # Make prediction
    result = esmfold_model.fold.remote(sequences)

    # Check output shape
    positions_shape = result.positions.shape

    # Assertions with detailed error messages
    # FIXME sequence len isn't matching
    # assert positions_shape[0] == len(sequences), \
    #     f"Batch size mismatch. Expected: {len(sequences)}, Got: {positions_shape[0]}"
    assert positions_shape[-1] == 3, f"Coordinate dimension mismatch. Expected: 3, Got: {positions_shape[-1]}"


def test_sequence_validation(esmfold_model: ESMFold):
    """Test sequence validation in FoldingAlgorithm."""

    # Test single sequence
    single_seq = TEST_SEQUENCES["short"]
    validated = esmfold_model._validate_sequences(single_seq)
    assert isinstance(validated, list), "Single sequence should be converted to list"
    assert len(validated) == 1, "Should contain one sequence"
    assert validated[0] == single_seq, "Sequence should be unchanged"

    # Test sequence list
    seq_list = [TEST_SEQUENCES["short"], TEST_SEQUENCES["medium"]]
    validated = esmfold_model._validate_sequences(seq_list)
    assert isinstance(validated, list), "Should return a list"
    assert len(validated) == 2, "Should contain two sequences"
    assert validated == seq_list, "Sequences should be unchanged"

    # Test invalid sequence
    with pytest.raises(ValueError) as exc_info:
        esmfold_model._validate_sequences(TEST_SEQUENCES["invalid"])
    assert "Invalid amino acid" in str(exc_info.value), f"Expected 'Invalid amino acid', got {str(exc_info.value)}"

    # Test that fold method uses validation
    with pytest.raises(ValueError) as exc_info:
        esmfold_model.fold.remote(TEST_SEQUENCES["invalid"])
    assert "Invalid amino acid" in str(exc_info.value), f"Expected 'Invalid amino acid', got {str(exc_info.value)}"


def test_esmfold_output_pdb_cif():
    """Test ESMFold output PDB and CIF."""

    with enable_output():
        with app.run():
            model = ESMFold(config={"output_pdb": True, "output_cif": False})
            # Define input sequences
            sequences = [TEST_SEQUENCES["short"], TEST_SEQUENCES["medium"]]
            result = model.fold.remote(sequences)

    assert result.pdb is not None, "PDB output should be generated"
    # assert result.cif is not None, "CIF output should be generated"

    assert isinstance(result.pdb, list), "PDB output should be a list"
    assert len(result.pdb) == len(sequences), "PDB output should have same length as input sequences"
    # assert isinstance(result.cif, list), "CIF output should be a list"
    # assert len(result.cif) == len(sequences), "CIF output should have same length as input sequences"

    # TODO: maybe do a proper validation of the PDB format, which would require biotite/biopython dependency
    # # Check CIF format
    # for cif_str in result.cif:
    #     assert cif_str.startswith("data_"), "CIF should start with data_"

    # for pdb_str, cif_str in zip(result.pdb, result.cif):
    #     # Count ATOM records (each line starting with ATOM is one atom)
    #     n_atoms_pdb = sum(1 for line in pdb_str.splitlines() if line.startswith("ATOM") and 'TER' not in line)
    #     # Count atoms in CIF (each row in _atom_site table represents one atom)
    #     n_atoms_cif = sum(1 for line in cif_str.splitlines() if line.strip() and not line.startswith("#") and not line.startswith("_"))
    #     assert n_atoms_pdb == n_atoms_cif, "PDB and CIF should have same number of atoms"

    # Check default config re-writing works
    with enable_output():
        with app.run():
            model = ESMFold(config={"output_pdb": True})
            result = model.fold.remote(TEST_SEQUENCES["short"])
            assert result.pdb is not None, "PDB output should be generated"
            assert result.cif is None, "CIF output should be None"

            assert isinstance(result.pdb, list), "PDB output should be a list"
            assert len(result.pdb) == 1, "PDB output should have same length as input sequences"


if __name__ == "__main__":
    test_esmfold_chain_indices()
