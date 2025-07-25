"""Social Media Geofenced Stream Integrations"""
import asyncio
import httpx
from websockets.client import connect

class TwitterDecahose:
    def __init__(self, api_key: str):
        self.base_url = "https://api.twitter.com/decahose/v1"
        self.api_key = api_key
    
    async def stream_geo_keywords(self, keywords: list, bbox: tuple):
        """Stream 10% of Twitter firehose with geo+keyword filtering"""
        params = {
            "keywords": ",".join(keywords),
            "bbox": ",".join(map(str, bbox))
        }
        headers = {"Authorization": f"Bearer {self.api_key}"}
        
        async with connect(
            "wss://stream.twitter.com/decahose/v1/geo",
            extra_headers=headers
        ) as ws:
            await ws.send(params)
            while True:
                yield await ws.recv()

class SnapMap:
    def __init__(self, auth_token: str):
        self.base_url = "https://map.snapchat.com/api"
        self.auth_token = auth_token
    
    async def get_public_stories(self, lat: float, lon: float, radius_km: int = 1):
        """Fetch public stories near location (unofficial API)"""
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/v1/stories",
                headers={"Authorization": f"Bearer {self.auth_token}"},
                params={
                    "lat": lat,
                    "lng": lon,
                    "radius": radius_km
                }
            )
            return response.json()
