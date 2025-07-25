import unittest
import os
import asyncio
from unittest.mock import patch
from core.enrichment.enrich import EnrichmentService

class TestIntegration(unittest.TestCase):
    @unittest.skipUnless(os.getenv("TEST_WITH_DB") == "true", "Requires infrastructure running")
    def test_full_enrichment_flow(self):
        """Test complete enrichment flow with all data sources"""
        # Mock event with minimal required fields
        test_event = {
            "plate": "6ABC123",
            "state": "CA",
            "location": {"lat": 37.7749, "lng": -122.4194},
            "radius_km": 1
        }
        
        # Initialize service
        service = EnrichmentService()
        
        # Run enrichment
        result = asyncio.run(service.enrich_event(test_event))
        
        # Verify basic fields
        self.assertIn("vin", result)
        self.assertIn("owner", result)
        self.assertIn("phone", result)
        self.assertIn("handles", result)
        
        # Verify social handles structure
        self.assertEqual(len(result["handles"]), 4)
        
        # Verify Neo4j connection by checking if data was stored
        with service.driver.session() as session:
            query = """
            MATCH (p:Person {phone: $phone})-[:OWNS]->(v:Vehicle {vin: $vin})
            RETURN count(*) AS count
            """
            count = session.run(query, {"phone": result["phone"], "vin": result["vin"]}).single()["count"]
            self.assertEqual(count, 1)

if __name__ == '__main__':
    unittest.main()
