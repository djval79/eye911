"""Municipal IoT Mesh Integrations"""
import asyncio
import httpx

class NoTraffic:
    def __init__(self, api_key: str):
        self.base_url = "https://api.notraffic.tech/v2"
        self.api_key = api_key
    
    async def get_trajectory_breaks(self, intersection_id: str):
        """Detect vehicle trajectory breaks from smart intersection lidar"""
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/intersections/{intersection_id}/events",
                headers={"Authorization": f"Bearer {self.api_key}"},
                params={"event_type": "trajectory_break"}
            )
            return response.json()

class Iteris:
    def __init__(self, client_id: str, client_secret: str):
        self.auth_url = "https://api.iteris.com/oauth/token"
        self.api_url = "https://api.iteris.com/vantage/v3"
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
    
    async def get_speed_dropouts(self, corridor_id: str):
        """Detect speed heat-map dropouts"""
        if not self.token:
            await self.authenticate()
            
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.api_url}/corridors/{corridor_id}/speed-dropouts",
                headers={"Authorization": f"Bearer {self.token}"}
            )
            return response.json()
