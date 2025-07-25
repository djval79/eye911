"""Alternative People-Graph APIs"""
import asyncio
import httpx

class FullContact:
    def __init__(self, api_key: str):
        self.base_url = "https://api.fullcontact.com/v4"
        self.api_key = api_key
    
    async def lookup_by_phone(self, phone: str):
        """Lookup social handles by phone number"""
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/person.enrich",
                headers={"Authorization": f"Bearer {self.api_key}"},
                json={
                    "phone": phone,
                    "dataFilter": "social"
                }
            )
            return response.json()

class TrestleIntelius:
    def __init__(self, api_key: str):
        self.base_url = "https://api.trestleiq.com/v2"
        self.api_key = api_key
    
    async def reverse_phone_lookup(self, phone: str):
        """Reverse phone to full identity"""
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/phone/{phone}",
                headers={"X-API-Key": self.api_key}
            )
            return response.json()
