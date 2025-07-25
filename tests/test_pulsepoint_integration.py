"""
PulsePoint Integration Tests
==========================

Tests the PulsePointIngestor implementation with mock data.
Run with: python tests/test_pulsepoint_integration.py
"""
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
from datetime import datetime
from pre911.core.pulsepoint_ingestor import PulsePointIngestor

class TestPulsePointIntegration(unittest.TestCase):
    def setUp(self):
        # Test both mock and dataset modes
        self.mock_ingestor = PulsePointIngestor(mock=True)
        self.dataset_ingestor = PulsePointIngestor(
            dataset_path=os.path.join(os.path.dirname(__file__), '..', 'data')
        )
    
    def test_ingest_returns_data(self):
        """Test basic ingest functionality"""
        # Mock mode should return 'pulsepoint'
        mock_result = self.mock_ingestor.ingest()
        self.assertEqual(mock_result['source'], 'pulsepoint')
        
        # Dataset mode should return 'pulsepoint_dataset'
        dataset_result = self.dataset_ingestor.ingest()
        self.assertEqual(dataset_result['source'], 'pulsepoint_dataset')
        
        # Both should have data
        self.assertIn('data', mock_result)
        self.assertIn('data', dataset_result)
        self.assertGreater(len(mock_result['data']), 0)
        self.assertGreater(len(dataset_result['data']), 0)
    
    def test_incident_structure(self):
        """Test incident data structure"""
        for ingestor in [self.mock_ingestor, self.dataset_ingestor]:
            result = ingestor.ingest()
            incident = result['data'][0]
            
            required_fields = ['id', 'timestamp', 'location', 'type', 'severity', 'units']
            for field in required_fields:
                self.assertIn(field, incident)
    
    def test_severity_values(self):
        """Test severity values are valid"""
        for ingestor in [self.mock_ingestor, self.dataset_ingestor]:
            result = ingestor.ingest()
            for incident in result['data']:
                self.assertTrue(0 <= incident['severity'] <= 4)
    
    def test_dataset_timestamps(self):
        """Test LAFD dataset timestamp formatting"""
        result = self.dataset_ingestor.ingest()
        for incident in result['data']:
            try:
                datetime.fromisoformat(incident['timestamp'])
            except ValueError:
                self.fail(f"Invalid timestamp format: {incident['timestamp']}")
    
    def test_dataset_field_mapping(self):
        """Test LAFD to PulsePoint field mapping"""
        result = self.dataset_ingestor.ingest()
        incident = result['data'][0]
        self.assertIn('raw', incident)  # Verify raw data preservation
        self.assertEqual(incident['units'], 1)  # Default units_responding

if __name__ == "__main__":
    unittest.main()
