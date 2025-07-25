"""Connected Car Side-Channel Integrations"""
import asyncio
import httpx

class Otonomo:
    def __init__(self, client_id: str, client_secret: str):
        self.auth_url = "https://auth.otonomo.io/oauth/token"
        self.api_url = "https://api.otonomo.io/data/v1"
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
                },
                headers={"Content-Type": "application/x-www-form-urlencoded"}
            )
            if response.status_code != 200:
                raise Exception(f"Auth failed: {response.text}")
            self.token = response.json().get("access_token")
    
    async def get_crash_events(self):
        """Fetch crash events from OEM telematics"""
        if not self.token:
            await self.authenticate()
            
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.api_url}/crash-events",
                headers={"Authorization": f"Bearer {self.token}"}
            )
            return response.json()

class Smartcar:
    def __init__(self, access_token: str):
        self.base_url = "https://api.smartcar.com/v2.0"
        self.access_token = access_token
    
    async def get_vehicle_events(self, vehicle_id: str):
        """Fetch sudden speed drops and ignition events"""
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/vehicles/{vehicle_id}/events",
                headers={"Authorization": f"Bearer {self.access_token}"}
            )
            return response.json()
