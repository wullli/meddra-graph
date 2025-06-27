from pathlib import Path

import pandas as pd
import pytest

from meddra_graph.meddra_loader import MedDRAData, MedDRALoader

TEST_TERMS = [
    # SOC (System Organ Classes)
    ("soc", "50000001", "Lorem ipsum dolor sit amet"),
    ("soc", "50000002", "Consectetur adipiscing elit"),
    ("soc", "50000003", "Sed do eiusmod tempor incididunt"),
    ("soc", "50000004", "Ut labore et dolore magna aliqua"),
    ("soc", "50000005", "Enim ad minim veniam quis"),
    # HLGT (High Level Group Terms)
    ("hlgt", "30000001", "Nostrud exercitation ullamco"),
    ("hlgt", "30000002", "Laboris nisi ut aliquip ex ea"),
    ("hlgt", "30000003", "Commodo consequat duis aute irure"),
    ("hlgt", "30000004", "Dolor in reprehenderit in voluptate"),
    ("hlgt", "30000005", "Velit esse cillum dolore eu fugiat"),
    # HLT (High Level Terms)
    ("hlt", "10000001", "Nulla pariatur excepteur sint occaecat"),
    ("hlt", "10000002", "Cupidatat non proident sunt in culpa"),
    ("hlt", "10000003", "Qui officia deserunt mollit anim id"),
    ("hlt", "10000004", "Est laborum lorem ipsum dolor sit"),
    ("hlt", "10000005", "Amet consectetur adipiscing elit sed"),
    # PT (Preferred Terms)
    ("pt", "40000001", "Do eiusmod tempor incididunt ut"),
    ("pt", "40000002", "Labore et dolore magna aliqua"),
    ("pt", "40000003", "Enim ad minim veniam quis nostrud"),
    ("pt", "40000004", "Exercitation ullamco laboris nisi"),
    ("pt", "40000005", "Ut aliquip ex ea commodo consequat"),
    # LLT (Lowest Level Terms) from file
    ("llt", "20000001", "Reprehenderit in voluptate velit esse"),
    ("llt", "20000002", "Cillum dolore eu fugiat nulla"),
    ("llt", "20000003", "Pariatur excepteur sint occaecat"),
    ("llt", "20000004", "Cupidatat non proident sunt in"),
    ("llt", "20000005", "Culpa qui officia deserunt mollit"),
]

NUMBER_OF_TEST_TERMS = len(TEST_TERMS)
NUMBER_OF_TEST_EDGES = 23


def _generate_test_ids() -> list[str]:
    """Generate test IDs like soc1, soc2, hlgt1, hlgt2, etc."""
    term_counts: dict[str, int] = {}
    ids: list[str] = []
    for term_level, _, _ in TEST_TERMS:
        term_counts[term_level] = term_counts.get(term_level, 0) + 1
        ids.append(f"{term_level}{term_counts[term_level]}")
    return ids


@pytest.fixture(name="meddra_data")
def meddra_data_fixture() -> MedDRAData:
    return MedDRALoader.load(Path(__file__).parent / "test_data")


def test_loading_passes() -> None:
    MedDRALoader.load(Path(__file__).parent / "test_data")


def test_version_loaded(meddra_data: MedDRAData) -> None:
    assert meddra_data.version == "99.0 TestLang Dummy Data Release"


def test_term_levels_loaded(meddra_data: MedDRAData) -> None:
    df = pd.DataFrame.from_records(list(meddra_data.terms.values()))
    assert len(df["term_type"].unique()) == 5
    assert set(df["term_type"].unique()) == {"soc", "hlgt", "hlt", "pt", "llt"}


def test_schema_levels_loaded(meddra_data: MedDRAData) -> None:
    assert len(meddra_data.schema) == 12
    assert all(fn in meddra_data.schema for fn in ["soc.asc", "hlgt.asc", "hlt.asc", "pt.asc", "llt.asc"])


def test_edges_loaded(meddra_data: MedDRAData) -> None:
    assert len(meddra_data.edges) == NUMBER_OF_TEST_EDGES


def test_edges_are_pairs(meddra_data: MedDRAData) -> None:
    assert all(len(e) == 2 for e in meddra_data.edges)


def test_terms_loaded(meddra_data: MedDRAData) -> None:
    assert len(meddra_data.terms) == NUMBER_OF_TEST_TERMS


def test_graph_nodes_loaded(meddra_data: MedDRAData) -> None:
    assert len(list(meddra_data.to_graph().nodes())) == NUMBER_OF_TEST_TERMS


def test_graph_edges_loaded(meddra_data: MedDRAData) -> None:
    assert len(list(meddra_data.to_graph().edges())) == NUMBER_OF_TEST_EDGES


def test_graph_term_definitions_correct(meddra_data: MedDRAData) -> None:
    """Test that each term has the correct definition/name in the loaded data."""
    g = meddra_data.to_graph()
    for term_type, term_code, expected_name in TEST_TERMS:
        assert g.nodes[term_code][f"{term_type}_code"] == term_code
        assert g.nodes[term_code][f"{term_type}_name"] == expected_name
        assert g.nodes[term_code]["term_type"] == term_type


def test_graph_roots_are_socs(meddra_data: MedDRAData) -> None:
    g = meddra_data.to_graph()
    assert all(g.nodes[n]["term_type"] == "soc" for n in g.nodes() if g.in_degree(n) == 0)
