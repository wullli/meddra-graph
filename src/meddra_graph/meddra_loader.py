import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Union, cast

import networkx as nx

DEFAULT_SCHEMA_PATH = Path(__file__).parent / "resources" / "meddra_schema_v28.json"


@dataclass
class MedDRAData:
    version: str
    schema: dict[str, dict[str, str]]
    terms: dict[str, dict[str, Any]]
    edges: list[tuple[str, str]]

    def to_graph(self) -> nx.DiGraph:
        g: nx.DiGraph = nx.DiGraph()
        g.add_nodes_from(self.terms.keys())
        g.add_edges_from(self.edges)
        nx.set_node_attributes(g, self.terms)
        return g


@dataclass
class _MedDRASchema:
    fields: dict[str, dict[str, str]]
    term_types: set[str]

    def __init__(self, schema_path: Union[str, Path]):
        with open(schema_path, "r", encoding="utf-8") as f:
            data = cast(dict[str, dict[str, dict[str, str]]], json.load(f))
            self.term_types = set(data["term_types"])
            self.fields = data["fields"]


class MedDRALoader:

    @classmethod
    def load(
        cls, meddra_directory_path: Union[str, Path], schema_path: Union[str, Path] = DEFAULT_SCHEMA_PATH
    ) -> MedDRAData:
        meddra_directory_path = Path(meddra_directory_path)
        assert meddra_directory_path.is_dir()

        schema = _MedDRASchema(schema_path)
        version = " ".join(cls._load_file(meddra_directory_path / "meddra_release.asc")[0]).strip()
        terms = cls._load_terms(meddra_directory_path, schema)
        edges = cls._load_edges(meddra_directory_path, schema)
        edges = edges.union(
            set(
                (term_data["pt_code"], llt_code)
                for llt_code, term_data in terms.items()
                if term_data["term_type"] == "llt"
            )
        )

        return MedDRAData(version=version, schema=schema.fields, terms=terms, edges=list(edges))

    @classmethod
    def _load_terms(
        cls,
        meddra_directory_path: Path,
        schema: _MedDRASchema,
    ) -> dict[str, dict[str, Any]]:
        terms = {}
        for file_path in meddra_directory_path.glob("*.asc"):
            if cls._is_term_file(file_path, schema):
                data = cls._load_file(file_path)
                file_name = file_path.name
                term_type = file_name.split(".")[0]

                for row in data:
                    if len(row) < len(schema.fields[file_name]):
                        raise ValueError(f"Invalid number of fields in {file_path}")

                    term_dict = dict(zip(schema.fields[file_name].keys(), row))
                    term_dict["term_type"] = term_type

                    first_field = list(schema.fields[file_name].keys())[0]
                    term_key = term_dict[first_field]
                    terms[term_key] = term_dict

        return terms

    @classmethod
    def _load_edges(cls, meddra_directory_path: Path, schema: _MedDRASchema) -> set[tuple[str, str]]:
        edges: set[tuple[str, str]] = set()
        for file_path in meddra_directory_path.glob("*.asc"):
            if cls._is_edge_file(file_path, schema):
                edges.update(cast(set[tuple[str, str]], cls._load_file(file_path)))
        return edges

    @staticmethod
    def _is_term_file(file_path: Path, schema: _MedDRASchema) -> bool:
        return file_path.name.split(".")[0] in schema.term_types

    @staticmethod
    def _is_edge_file(file_path: Path, schema: _MedDRASchema) -> bool:
        if not "_" in file_path.name:
            return False
        try:
            t0, t1 = file_path.name.split(".")[0].split("_")
            return t0 in schema.term_types and t1 in schema.term_types
        except (ValueError, IndexError):
            return False

    @classmethod
    def _load_file(cls, file_path: Path) -> list[tuple[str, ...]]:
        lines = []
        with open(file_path, "r", encoding="utf-8") as f:
            for line in f:
                lines.append(cls._load_line(line))
        return lines

    @classmethod
    def _load_line(cls, line: str) -> tuple[str, ...]:
        return tuple(line.strip().split("$"))[:-1]  # there is always $ at the end of the line
