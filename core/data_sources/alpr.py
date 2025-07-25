"""ALPR (Automatic License Plate Recognition) Integrations"""
import asyncio
import httpx

class RekorScout:
    def __init__(self, api_key: str):
        self.base_url = "https://api.rekor.ai/v1"
        self.api_key = api_key
    
    async def get_plate_reads(self, bbox: tuple, max_age_ms: int = 500):
        """Fetch recent plate reads within bounding box"""
        params = {
            "bbox": ",".join(map(str, bbox)),
            "max_age_ms": max_age_ms
        }
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/scout/reads",
                headers={"Authorization": f"Bearer {self.api_key}"},
                params=params
            )
            return response.json()

class VigilantLEARN:
    def __init__(self, agency_id: str, auth_token: str):
        self.base_url = "https://api.vigilantsolutions.com/learn/v2"
        self.agency_id = agency_id
        self.auth_token = auth_token
    
    async def query_plates(self, plates: list, radius_miles: int = 1):
        """Query plates with ultra-low latency (LEO only)"""
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/query",
                headers={"X-Agency-ID": self.agency_id,
                        "X-Auth-Token": self.auth_token},
                json={
                    "plates": plates,
                    "radius_miles": radius_miles,
                    "max_age_ms": 100
                }
            )
            return response.json()
