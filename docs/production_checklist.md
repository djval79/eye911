# Production Deployment Checklist

## Before Deployment
- [ ] Obtain all API keys
  - NHTSA
  - PulsePoint
  - TomTom
  - Twitter
- [ ] Configure `.env` file with all keys
- [ ] Set `MOCK_MODE=False`
- [ ] Verify all tests pass with real keys

## Deployment Steps
1. Build Docker images
2. Configure Kubernetes secrets
3. Deploy Helm charts
4. Verify services are running

## Post-Deployment
- [ ] Monitor API rate limits
- [ ] Set up alerts for failed ingests
- [ ] Schedule regular database backups

## Rollback Plan
1. Scale down new deployment
2. Scale up previous version
3. Investigate issues

## Maintenance
- Monthly: Review API usage
- Quarterly: Rotate API keys
- As needed: Update dependencies
