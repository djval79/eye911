# Real Data Testing Procedure

## Preparation
1. Add API keys to `.env`:
   ```
   NHTSA_API_KEY=your_key
   PULSEPOINT_API_KEY=your_key
   MOCK_MODE=False
   ```
2. Verify database connection

## Test Cases
### NHTSA API
```bash
python tests/test_nhtsa_integration.py --real
```
- Verify:
  - Case listings return valid data
  - Location queries return geo-specific results
  - Data matches expected schema

### PulsePoint API
```bash
python tests/test_pulsepoint_integration.py --real
```
- Verify:
  - Active incidents returned
  - Severity mapping correct
  - Location data valid

## Monitoring
- Check API rate limits
- Verify error handling
- Monitor data freshness

## Expected Timeline
1. Initial smoke tests: 1 hour
2. Full validation: 4 hours
3. Ongoing monitoring: Daily
