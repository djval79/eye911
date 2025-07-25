# FARS Dataset Integration Guide

This document explains how to use NHTSA's Fatality Analysis Reporting System (FARS) datasets as an alternative to the live API.

## Setup

1. Download FARS datasets from [NHTSA's website](https://www.nhtsa.gov/research-data/fatality-analysis-reporting-system-fars)
2. Place CSV files in `/data/fars/` directory
3. Configure NHTSAIngestor to use dataset mode:

```python
# Use dataset mode when initializing
from pre911.core.nhtsa_ingestor import NHTSAIngestor

ingestor = NHTSAIngestor(data_dir="/path/to/fars/data")
```

## Data Format

The system expects FARS CSV files in the format:
- `FARS[YEAR]_National.csv` (e.g. `FARS2023_National.csv`)
- Standard FARS column names

## Validation

To verify data quality:
```python
result = ingestor.get_case_list(states=[6], from_year=2023, to_year=2023)
print(f"Found {len(result['data'])} crashes from dataset") 
```
