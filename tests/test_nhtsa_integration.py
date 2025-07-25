"""
NHTSA Integration Tests
======================

Demonstrates all NHTSAIngestor capabilities with mock data.
Run with: python -m tests.test_nhtsa_integration
"""
import sys
import os
import tempfile
import csv
import shutil
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
from pre911.core.nhtsa_ingestor import NHTSAIngestor

class TestNHTSAIntegration(unittest.TestCase):
    def setUp(self):
        self.ingestor = NHTSAIngestor(mock=True)
    
    def test_case_list(self):
        """Test getting crash case listings"""
        result = self.ingestor.get_case_list(
            states=[6],  # California
            from_year=2023,
            to_year=2024
        )
        self.assertIn('data', result)
        self.assertGreater(len(result['data']), 0)
    
    def test_case_details(self):
        """Test getting crash details"""
        result = self.ingestor.get_case_details(
            state_case='12345',
            case_year=2024,
            state=6
        )
        self.assertIn('data', result)
        self.assertEqual(result['data'][0]['stateCase'], '12345')
        self.assertEqual(result['data'][0]['state'], 6)
    
    def test_location_queries(self):
        """Test geographic crash queries"""
        # State-wide
        result = self.ingestor.get_crashes_by_location(state=6)
        self.assertIn('data', result)
        
        # County-specific
        result = self.ingestor.get_crashes_by_location(
            state=6,
            county=37  # Los Angeles
        )
        self.assertIn('data', result)
    
    def test_default_ingest(self):
        """Test the default ingest method"""
        result = self.ingestor.ingest()
        self.assertIn('data', result)
        self.assertGreater(len(result['data']), 0)

if __name__ == "__main__":
    unittest.main()
