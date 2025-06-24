# MedDRA Test Data

This directory contains dummy test data files for testing the MedDRADiGraph loading functionality.

## Important Note

**All data in these files is completely anonymized and fake.** This includes:
- Lorem Ipsum text for all term names and descriptions
- Anonymized codes (e.g., ABC, DEF, PQR instead of real abbreviations)
- Fake version numbers (99.0 instead of real MedDRA versions)
- Generic ICD codes (X00-X99, Y00-Y99, Z00-Z99 instead of real medical codes)
- Anonymized reference codes for all external coding systems

This ensures no real MedDRA data is stored in this repository, which is important for licensing compliance.

## Data Format

All files use the MedDRA standard format (version 28.0):
- Fields are delimited by `$` characters
- Each line represents one record
- Field structure follows the schema defined in `src/meddra_loader/resources/meddra_schema_v28.json`

