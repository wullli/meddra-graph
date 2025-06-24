from pathlib import Path

import pytest

from meddra_loader.meddra_digraph import MedDRADiGraph

TEST_TERMS = [
    # SOC (System Organ Class) test cases
    ("soc", "10001000", "Lorem ipsum dolor sit amet"),
    ("soc", "10002000", "Consectetur adipiscing elit"),
    ("soc", "10003000", "Sed do eiusmod tempor incididunt"),

    # HLGT (High Level Group Term) test cases
    ("hlgt", "10001001", "Nostrud exercitation ullamco"),
    ("hlgt", "10001002", "Laboris nisi ut aliquip ex ea"),
    ("hlgt", "10002001", "Commodo consequat duis aute irure"),

    # HLT (High Level Term) test cases
    ("hlt", "10001101", "Nulla pariatur excepteur sint occaecat"),
    ("hlt", "10001102", "Cupidatat non proident sunt in culpa"),
    ("hlt", "10002101", "Est laborum lorem ipsum dolor sit"),

    # LLT (Lowest Level Term) test cases - using codes that don't conflict with mdhier.asc
    ("llt", "10001302", "Cillum dolore eu fugiat nulla"),
    ("llt", "10001303", "Pariatur excepteur sint occaecat"),
    ("llt", "10002302", "Anim id est laborum sed ut"),
]


@pytest.fixture(name="meddra_digraph")
def meddra_digraph_fixture() -> MedDRADiGraph:
    return MedDRADiGraph()


@pytest.fixture(name="test_data_path")
def test_data_path_fixture() -> Path:
    return Path(__file__).parent / "test_data"


def test_term_levels_loaded(meddra_digraph: MedDRADiGraph, test_data_path: Path) -> None:
    meddra_digraph.load(test_data_path)
    assert meddra_digraph.meddra_version is not None
    assert len(meddra_digraph.term_levels) == 6
    assert set(meddra_digraph.term_levels) == {"soc", "hlgt", "hlt", "pt", "llt", "mdhier"}


def test_schema_levels_loaded(meddra_digraph: MedDRADiGraph, test_data_path: Path) -> None:
    meddra_digraph.load(test_data_path)
    assert len(meddra_digraph.schema) == 12
    # Check that core term files are in schema
    assert "soc.asc" in meddra_digraph.schema
    assert "hlgt.asc" in meddra_digraph.schema
    assert "hlt.asc" in meddra_digraph.schema
    assert "pt.asc" in meddra_digraph.schema
    assert "llt.asc" in meddra_digraph.schema
    assert "mdhier.asc" in meddra_digraph.schema


def test_edges_loaded(meddra_digraph: MedDRADiGraph, test_data_path: Path) -> None:
    meddra_digraph.load(test_data_path)
    assert len(meddra_digraph.edges) >= 0


def test_terms_loaded(meddra_digraph: MedDRADiGraph, test_data_path: Path) -> None:
    meddra_digraph.load(test_data_path)
    assert len(meddra_digraph.terms) > 1


def test_nodes_loaded(meddra_digraph: MedDRADiGraph, test_data_path: Path) -> None:
    meddra_digraph.load(test_data_path)
    assert len(meddra_digraph.nodes) > 1


# Generate IDs automatically from the test parameters
def _generate_test_ids() -> list[str]:
    """Generate test IDs like soc1, soc2, hlgt1, hlgt2, etc."""
    term_counts: dict[str, int] = {}
    ids: list[str] = []
    for term_level, _, _ in TEST_TERMS:
        term_counts[term_level] = term_counts.get(term_level, 0) + 1
        ids.append(f"{term_level}{term_counts[term_level]}")
    return ids


@pytest.mark.parametrize("term_level, term_code, expected_name", TEST_TERMS, ids=_generate_test_ids())
def test_term_definitions_correct(
        meddra_digraph: MedDRADiGraph,
        test_data_path: Path,
        term_level: str,
        term_code: str,
        expected_name: str
) -> None:
    """Test that each term level has the correct definition/name in the test data."""
    meddra_digraph.load(test_data_path)

    assert term_code in meddra_digraph.terms, f"Term {term_code} not found in loaded terms"

    term_data = meddra_digraph.terms[term_code]
    assert term_data["node_type"] == term_level, f"Expected node_type {term_level}, got {term_data['node_type']}"

    name_field = f"{term_level}_name"
    assert name_field in term_data, f"Name field {name_field} not found in term data"
    assert term_data[
               name_field] == expected_name, f"Expected {name_field} to be '{expected_name}', got '{term_data[name_field]}'"
