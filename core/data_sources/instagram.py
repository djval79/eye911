"""Instagram Enrichment Integrations"""
import asyncio
import httpx

class SocialLinks:
    def __init__(self, api_key: str):
        self.base_url = "https://api.sociallinks.io/v3"
        self.api_key = api_key
    
    async def lookup_handles(self, identifiers: list):
        """Lookup social handles from various identifiers"""
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/lookup",
                headers={"X-API-Key": self.api_key},
                json={"identifiers": identifiers}
            )
            return response.json()

class PathSocial:
    def __init__(self, client_id: str, client_secret: str):
        self.auth_url = "https://api.pathsocial.com/oauth/token"
        self.api_url = "https://api.pathsocial.com/graphql"
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
    
    async def query_profile(self, username: str):
        """Query Instagram profile via GraphQL"""
        if not self.token:
            await self.authenticate()
            
        query = """
        query Profile($username: String!) {
            instagramProfile(username: $username) {
                username
                fullName
                followers
                posts {
                    edges {
                        node {
                            id
                            caption
                            location
                        }
                    }
                }
            }
        }
        """
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                self.api_url,
                headers={"Authorization": f"Bearer {self.token}"},
                json={"query": query, "variables": {"username": username}}
            )
            return response.json()
