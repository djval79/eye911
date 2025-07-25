"""911 CAD Firehose Integrations"""
import asyncio
import httpx
from websockets.client import connect

class PulsePoint:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.pulsepoint.org/v1"
    
    async def get_live_incidents(self):
        """Fetch live incidents via REST API"""
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/incidents",
                headers={"Authorization": f"Bearer {self.api_key}"}
            )
            return response.json()
    
    async def stream_incidents(self):
        """Stream incidents via websocket"""
        async with connect("wss://stream.pulsepoint.org/v1/ws") as ws:
            await ws.send(self.api_key)
            while True:
                yield await ws.recv()

class RapidDeploy:
    def __init__(self, webhook_url: str):
        self.webhook_url = webhook_url
    
    async def handle_webhook(self, request):
        """Process incoming webhook from RapidDeploy"""
        data = await request.json()
        return {"status": "received", "incident_id": data.get("id")}
