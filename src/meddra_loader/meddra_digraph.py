import json
from pathlib import Path
from typing import Any, Union, cast

import networkx as nx

DEFAULT_SCHEMA_PATH = Path(__file__).parent / "resources" / "meddra_schema_v28.json"


class MedDRADiGraph(nx.DiGraph):

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.schema: dict[str, dict[str, str]] = {}
        self.term_levels: set[str] = set()
        self.edges: set[tuple[str, ...]] = set()
        self.terms: dict[str, dict[str, Any]] = {}
        self.meddra_version: Union[str, None] = None

    def load(
            self, meddra_directory_path: Union[str, Path],
            schema_path: Union[str, Path] = DEFAULT_SCHEMA_PATH
    ) -> None:
        meddra_directory_path = Path(meddra_directory_path)
        self.schema = self._load_schema(schema_path)
        self.meddra_version = " ".join(self._load_file(meddra_directory_path / "meddra_release.asc")[0]).strip()
        assert meddra_directory_path.is_dir()
        self.term_levels = self._get_term_levels(meddra_directory_path)
        edges = set()
        self.terms = {}
        for file_path in meddra_directory_path.glob("*.asc"):
            if self._is_edge_file(file_path):
                edges.update(self._load_file(file_path))

        for file_path in meddra_directory_path.glob("*.asc"):
            if self._is_term_file(file_path):
                data = self._load_file(file_path)
                file_name = file_path.name
                node_type = file_path.name.split(".")[0]

                # Process each row of data
                for row in data:
                    if len(row) >= len(self.schema[file_name]):
                        # Create a dictionary for this term using the schema
                        term_dict = dict(zip(self.schema[file_name].keys(), row))
                        term_dict["node_type"] = node_type

                        # Use the first field as the key (usually the code)
                        first_field = list(self.schema[file_name].keys())[0]
                        term_key = term_dict[first_field]
                        self.terms[term_key] = term_dict
        self.add_edges_from(edges)
        self.add_nodes_from(self.terms.keys())
        nx.set_node_attributes(self, self.terms)

    def _load_schema(self, schema_path: Union[str, Path]) -> dict[str, dict[str, str]]:
        with open(schema_path, "r", encoding="utf-8") as f:
            return cast(dict[str, dict[str, str]], json.load(f))

    def _get_term_levels(self, meddra_directory_path: Path) -> set[str]:
        term_levels = set()
        for file_path in meddra_directory_path.glob("*.asc"):
            file_name = file_path.name.split(".")[0]
            if not "_" in file_name:
                term_levels.add(file_name)
        return term_levels

    def _is_term_file(self, file_path: Path) -> bool:
        return file_path.name.split(".")[0] in self.term_levels

    def _is_edge_file(self, file_path: Path) -> bool:
        if not "_" in file_path.name:
            return False
        try:
            t0, t1 = file_path.name.split(".")[0].split("_")
            return t0 in self.term_levels and t1 in self.term_levels
        except (ValueError, IndexError):
            return False

    def _load_file(self, file_path: Path) -> list[tuple[str, ...]]:
        lines = []
        with open(file_path, "r", encoding="utf-8") as f:
            for line in f:
                lines.append(self._load_line(line))
        return lines

    def _load_line(self, line: str) -> tuple[str, ...]:
        return tuple(line.strip().split("$"))
