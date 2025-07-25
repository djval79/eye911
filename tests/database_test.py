import unittest
import os
from neo4j import GraphDatabase

class TestDatabaseConnection(unittest.TestCase):
    @unittest.skipUnless(os.getenv("TEST_WITH_DB") == "true", "Requires Neo4j running")
    def test_neo4j_connection(self):
        """Test basic connection to Neo4j (only runs when TEST_WITH_DB=true)"""
        try:
            driver = GraphDatabase.driver(
                "bolt://localhost:7687",
                auth=("neo4j", "password")
            )
            with driver.session() as session:
                result = session.run("RETURN 1 AS x")
                self.assertEqual(result.single()["x"], 1)
        except Exception as e:
            self.fail(f"Database connection failed: {str(e)}")

if __name__ == '__main__':
    unittest.main()
