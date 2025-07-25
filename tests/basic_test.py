import unittest
import sys
from pathlib import Path

# Add mock path
sys.path.insert(0, str(Path(__file__).parent))
from mocks.enrichment import enrich

class TestBasicFunctionality(unittest.TestCase):
    def test_enrichment_logic(self):
        """Test core enrichment logic with mocks"""
        test_msg = {
            "plate": "ABC1234",
            "state": "NY"
        }
        
        import asyncio
        result = asyncio.run(enrich(test_msg))
        
        self.assertEqual(result["fname"], "Jane")
        self.assertEqual(result["lname"], "Doe")
        self.assertEqual(result["phone"], "+15551234567")

if __name__ == '__main__':
    unittest.main()
