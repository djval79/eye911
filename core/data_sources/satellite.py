"""Satellite RF Glint Integrations"""
import asyncio
import httpx

class CapellaSpace:
    def __init__(self, api_key: str):
        self.base_url = "https://api.capellaspace.com/v1"
        self.api_key = api_key
    
    async def detect_vehicle_deformation(self, coordinates: list):
        """Detect vehicle deformation via SAR imagery"""
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/sar/vehicle-detection",
                headers={"Authorization": f"Bearer {self.api_key}"},
                json={"coordinates": coordinates}
            )
            return response.json()

class ICEYE:
    def __init__(self, client_id: str, client_secret: str):
        self.auth_url = "https://auth.iceye.com/oauth/token"
        self.api_url = "https://api.iceye.com/v1"
        self.client_id = client_id
        self.client_secret = client_secret
        self.token = None
    
    async def authenticate(self):
        """Get OAuth2 token"""
        async with httpx.AsyncClient() as client:
            response = await client.post(
                self.auth_url,
                data={
                    "client_id": self.client_id,
                    "client_secret": self.client_secret,
                    "grant_type": "client_credentials"
                }
            )
            self.token = response.json().get("access_token")
    
    async def detect_highway_changes(self, segment_id: str):
        """Detect changes on highway segments"""
        if not self.token:
            await self.authenticate()
            
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.api_url}/highway/{segment_id}/changes",
                headers={"Authorization": f"Bearer {self.token}"}
            )
            return response.json()
