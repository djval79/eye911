"""Cell Location Doppler Integrations"""
import asyncio
import httpx

class LocationSmart:
    def __init__(self, carrier_token: str):
        self.base_url = "https://api.locationsmart.com/v3"
        self.carrier_token = carrier_token
    
    async def get_velocity_vectors(self, cell_ids: list):
        """Fetch handset velocity vectors from carrier data"""
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/velocity/vectors",
                headers={"X-Carrier-Token": self.carrier_token},
                json={"cell_ids": cell_ids}
            )
            return response.json()

class XMode:
    def __init__(self, sdk_key: str):
        self.base_url = "https://api.xmode.io/v1"
        self.sdk_key = sdk_key
    
    async def detect_sudden_stops(self, device_ids: list, min_g_force: float = 8.0):
        """Detect sudden stops from SDK ping data"""
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/events/sudden-stop",
                headers={"X-SDK-Key": self.sdk_key},
                json={
                    "device_ids": device_ids,
                    "min_g_force": min_g_force
                }
            )
            return response.json()
