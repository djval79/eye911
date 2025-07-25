# API Integration Guide

## NHTSA API

### Configuration
1. Add your NHTSA API key to `.env`:
   ```
   NHTSA_API_KEY=your_key_here
   ```
2. Set `MOCK_MODE=False` in production

### Dataset Mode (When API Keys Unavailable)
```python
# Initialize with FARS dataset directory
from pre911.core.nhtsa_ingestor import NHTSAIngestor

ingestor = NHTSAIngestor(data_dir="/path/to/fars/data")
```

### Endpoints
- `get_case_list()`: Retrieve crash listings
- `get_case_details()`: Get detailed crash reports
- `get_crashes_by_location()`: Geographic queries

## PulsePoint API Integration

### Configuration
1. Add your PulsePoint key to `.env`:
   ```
   PULSEPOINT_API_KEY=your_key_here
   ```
2. Set `MOCK_MODE=False` in production

### Dataset Mode

When API keys are unavailable, the PulsePointIngestor can operate in dataset mode using local CSV files:

```python
from pre911.core.pulsepoint_ingestor import PulsePointIngestor

# Initialize with dataset path
ingestor = PulsePointIngestor(dataset_path='/path/to/data/directory')

# Ingest data - returns {'source': 'pulsepoint_dataset', 'data': [...]}
result = ingestor.ingest()
```

### Requirements
#### CSV File Requirements
- CSV files must be named `pulsepoint_incidents_YYYY-MM-DD.csv`
- Must contain required fields: incident_id, incident_type, timestamp, latitude, longitude
- Timestamps must be in ISO 8601 format with timezone

#### Output Format
- Source field will be 'pulsepoint_dataset' (vs 'pulsepoint' for mock/API modes)
- Data structure matches live API response format

## Testing
```bash
# Run all tests
python -m unittest discover tests

# Test FARS dataset integration
python tests/test_fars_dataset.py
