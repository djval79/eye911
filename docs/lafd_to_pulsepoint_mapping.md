# LAFD Response Metrics to PulsePoint Data Mapping Specification

## Field Mappings

| LAFD Field | PulsePoint Field | Transformation Logic | Notes |
|-----------|------------------|----------------------|-------|
| Randomized Incident Number | incident_id | Direct mapping | Must be unique |
| Time of Dispatch (GMT) | timestamp | Parse GMT time + current date | Format: ISO 8601 with timezone |
| Emergency Dispatch Code | incident_type | Title case conversion | |
| Emergency Dispatch Code | severity | 4 if contains 'Emergency', else 2 | |
| (Default) | units_responding | Default to 1 | LAFD doesn't provide unit count |
| First In District | raw_data | Direct mapping | For reference |

## Validation Rules

1. **Required Fields**:
   - incident_id must be present and non-empty
   - timestamp must be valid ISO 8601 format
   
2. **Data Quality Checks**:
   - Emergency Dispatch Code should match known patterns
   - Timestamps should be within reasonable time ranges

## Sample Transformation

```python
# Example transformation logic
def transform_row(lafd_row):
    today = datetime.now(timezone.utc).date()
    dispatch_time = datetime.strptime(
        lafd_row['Time of Dispatch (GMT)'].split('.')[0], 
        '%H:%M:%S'
    ).time()
    
    return {
        'incident_id': lafd_row['Randomized Incident Number'],
        'timestamp': datetime.combine(today, dispatch_time).isoformat(),
        'incident_type': lafd_row['Emergency Dispatch Code'].title(),
        'severity': 4 if 'Emergency' in lafd_row['Emergency Dispatch Code'] else 2,
        'units_responding': 1,
        'raw_data': lafd_row.get('First In District', '')
    }
```
