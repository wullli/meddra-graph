

# MedDRA Loader

[![CI](https://github.com/wullli/meddra-loader/workflows/CI/badge.svg)](https://github.com/wullli/meddra-loader/actions/workflows/ci.yml)
[![codecov](https://codecov.io/gh/wullli/meddra-loader/branch/main/graph/badge.svg)](https://codecov.io/gh/wullli/meddra-loader)

DISCLAIMER: This software does not give you access to MedDRA and you need a valid subscription to work with MedDRA data: https://www.meddra.org/. It merely provides tooling for loading the MedDRA data and hierarchy with python into a networkx graph. It is only intended for use with legitimately licensed MedDRA data and users are responsible for obtaining a valid license from the MSSO.

## Usage

### MedDRALoader

The `MedDRALoader` class provides functionality to load MedDRA data from standard MedDRA files:

```python
from pathlib import Path
from meddra_graph.meddra_loader import MedDRALoader

# Path to your MedDRA data directory
meddra_path = Path("/path/to/meddra/data")

# Load MedDRA data
meddra_data = MedDRALoader.load(meddra_path)

# Access loaded data
print(f"MedDRA Version: {meddra_data.version}")
print(f"Number of terms: {len(meddra_data.terms)}")

# Convert to NetworkX DiGraph
graph = meddra_data.to_graph()
```
