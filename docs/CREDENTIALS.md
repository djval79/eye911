# Credential Management Guide

## Otonomo
1. Log in to Otonomo Developer Portal
2. Navigate to Applications > Your App
3. Generate new client credentials
4. Verify auth endpoint: `https://auth.otonomo.io/oauth/token`

## Smartcar
1. Access Smartcar Dashboard
2. Go to Applications > Your App
3. Generate new access token
4. Required scopes: `read_vehicle_info read_location`

## Update Procedure
1. Test new credentials with test scripts
2. Update workspace.yml secrets
3. Rotate credentials in production deployment
