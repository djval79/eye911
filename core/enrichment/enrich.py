import asyncio
import os
from neo4j import GraphDatabase
from ..data_sources.manager import DataSourceManager

# Updated connection configuration
NEO4J = GraphDatabase.driver(
    os.getenv("NEO4J_URI", "bolt://localhost:7687"),
    auth=("neo4j", os.getenv("NEO4J_PASS", "password"))
)

KAFKA = os.getenv("KAFKA_BROKERS")

class EnrichmentService:
    def __init__(self):
        """Initialize with all data sources"""
        self.driver = NEO4J
        self.data_sources = DataSourceManager({
            # All config comes from environment variables
            key.lower(): os.getenv(key)
            for key in [
                "PULSEPOINT_API_KEY", "RAPIDDEPLOY_WEBHOOK_URL",
                "OTONOMO_CLIENT_ID", "OTONOMO_CLIENT_SECRET",
                "SMARTCAR_ACCESS_TOKEN", "REKOR_API_KEY",
                "VIGILANT_AGENCY_ID", "VIGILANT_AUTH_TOKEN",
                "LOCATIONSMART_TOKEN", "XMODE_SDK_KEY",
                "TWITTER_API_KEY", "SNAPCHAT_AUTH_TOKEN",
                "CAPELLA_API_KEY", "ICEYE_CLIENT_ID",
                "ICEYE_CLIENT_SECRET", "NOTRAFFIC_API_KEY",
                "ITERIS_CLIENT_ID", "ITERIS_CLIENT_SECRET",
                "FULLCONTACT_API_KEY", "TRESTLE_API_KEY",
                "SOCIALLINKS_API_KEY", "PATHSOCIAL_CLIENT_ID",
                "PATHSOCIAL_CLIENT_SECRET"
            ]
        })

    async def enrich_event(self, event):
        """Main enrichment pipeline"""
        # 1. Detect crash signals from all sources
        crash_signals = await self.data_sources.detect_crash_signals(
            event["location"],
            event.get("radius_km", 1)
        )
        
        # 2. If plate available, resolve identity
        if "plate" in event:
            identity = await self._resolve_identity(event["plate"])
            event.update(identity)
        
        # 3. Store in Neo4j
        await self._store_in_graph(event, crash_signals)
        
        return event

    async def _resolve_identity(self, plate):
        """Resolve identity using all available data sources"""
        # First get VIN and owner info
        vin, owner = await self._vin_lookup(plate)
        
        # Then get phone number
        phone = await self._phone_from_vin(vin)
        
        # Finally get social handles using our new data sources
        identity_data = await self.data_sources.enrich_identity({
            "phone": phone,
            "vin": vin,
            "plate": plate
        })
        
        return {
            "vin": vin,
            "owner": owner,
            "phone": phone,
            "handles": identity_data.get("instagram", []) + identity_data.get("people_graph", [])
        }

    async def _store_in_graph(self, event, crash_signals):
        with self.driver.session() as s:
            s.run("""
            MERGE (p:Person {phone:$phone})
            SET p.fname=$fname, p.lname=$lname
            MERGE (v:Vehicle {vin:$vin})
            MERGE (p)-[:OWNS]->(v)
            MERGE (t:Twitter {handle:$t})
            MERGE (i:Instagram {handle:$i})
            MERGE (f:Facebook {handle:$f})
            MERGE (s:Snapchat {handle:$s})
            MERGE (p)-[:HAS]->(t),(p)-[:HAS]->(i),(p)-[:HAS]->(f),(p)-[:HAS]->(s)
            """, phone=event["phone"], fname=event["owner"]["fname"], lname=event["owner"]["lname"],
            vin=event["vin"], t=event["handles"][0], i=event["handles"][1], f=event["handles"][2], s=event["handles"][3])

async def enrich(msg):
    service = EnrichmentService()
    return await service.enrich_event(msg)

if __name__ == "__main__":
    from aiokafka import AIOKafkaConsumer
    asyncio.run(AIOKafkaConsumer("crash-alert", bootstrap_servers=KAFKA, value_deserializer=lambda m: json.loads(m.decode())).start())
