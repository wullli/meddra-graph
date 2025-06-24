#!/usr/bin/env python3
"""
Demo script to show MedDRADiGraph loading dummy data.
"""

from pathlib import Path
from src.meddra_loader.meddra_digraph import MedDRADiGraph

def main():
    # Create MedDRADiGraph instance
    graph = MedDRADiGraph()
    
    # Load dummy test data
    test_data_path = Path("src/meddra_loader/tests/test_data")
    print(f"Loading dummy MedDRA data from: {test_data_path}")
    
    graph.load(test_data_path)
    
    # Display loaded information
    print(f"\nMedDRA Version: {graph.meddra_version}")
    print(f"Term Levels: {graph.term_levels}")
    print(f"Number of terms loaded: {len(graph.terms)}")
    print(f"Schema files: {list(graph.schema.keys())}")
    
    # Show some sample terms
    print("\nSample terms loaded:")
    for i, (term_id, term_data) in enumerate(graph.terms.items()):
        if i >= 5:  # Show only first 5 terms
            break
        print(f"  {term_id}: {term_data}")
    
    print("\nDummy data loading completed successfully!")

if __name__ == "__main__":
    main()
