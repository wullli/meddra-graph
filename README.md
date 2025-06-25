

# MedDRA Loader

[![CI](https://github.com/wullli/meddra-loader/workflows/CI/badge.svg)](https://github.com/wullli/meddra-loader/actions/workflows/ci.yml)
[![codecov](https://codecov.io/gh/wullli/meddra-graph/graph/badge.svg?token=GN9CVJ0X0M)](https://codecov.io/gh/wullli/meddra-graph)

DISCLAIMER: This software does not give you access to MedDRA and you need a valid subscription to work with MedDRA data: https://www.meddra.org/. It merely provides tooling for loading the MedDRA data and hierarchy with python into a networkx graph. It is only intended for use with legitimately licensed MedDRA data and users are responsible for obtaining a valid license from the MSSO.

## Usage

### Schema

Since MedDRA raw data files do not contain schema information, it is necessary to provide a file that describes the schema of the MedDRA data. 
This repository contains a schema file for MedDRA version 28.0 (`src/meddra_graph/resources/meddra_schema_v28.json`) that can be used as a starting point.

### MedDRALoader

The `MedDRALoader` class provides functionality to load MedDRA data from standard MedDRA files:

```python
from pathlib import Path
from meddra_graph.meddra_loader import MedDRALoader

# Path to your MedDRA data directory
meddra_path = Path("/path/to/meddra/data")
schema_path = Path(__file__).parent / "resources" / "meddra_schema_v28.json" # optional, defaults to this

# Load MedDRA data
meddra_data = MedDRALoader.load(meddra_path, schema_path=schema_path)

# Access loaded data
print(f"MedDRA Version: {meddra_data.version}")
print(f"Number of terms: {len(meddra_data.terms)}")

# Convert to NetworkX DiGraph
graph = meddra_data.to_graph()
```
