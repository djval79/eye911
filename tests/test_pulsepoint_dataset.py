"""Tests for PulsePoint dataset integration"""
import os
import tempfile
import csv
import shutil
import unittest
from typing import Dict, Any, List

# Import only what we need to avoid circular imports
from pre911.core.pulsepoint_ingestor import PulsePointIngestor, PulsePointDatasetParser

class TestPulsePointDatasetIntegration(unittest.TestCase):
    """Tests for PulsePoint dataset integration"""
    
    @classmethod
    def setUpClass(cls):
        # Create a temporary test dataset directory
        cls.test_dir = tempfile.mkdtemp()
        cls.test_file = os.path.join(cls.test_dir, 'incidents_2023.csv')
        
        # Create a sample dataset file
        with open(cls.test_file, 'w') as f:
            writer = csv.writer(f)
            writer.writerow(['incident_id','timestamp','longitude','latitude',
                           'incident_type','severity','units_responding'])
            writer.writerow(['PP-1001','2023-01-15T08:30:00',-118.2437,34.0522,'Traffic',2,2])
            writer.writerow(['PP-1002','2023-02-20T14:15:00',-118.2550,34.0450,'Medical',3,1])
            writer.writerow(['PP-1003','2023-03-10T12:00:00',-118.5000,34.1000,'Fire',4,3])
    
    @classmethod
    def tearDownClass(cls):
        # Clean up test directory
        shutil.rmtree(cls.test_dir)
    
    def test_dataset_loading(self):
        """Test loading dataset files"""
        parser = PulsePointDatasetParser(self.test_dir)
        self.assertEqual(len(parser.data), 3)
        
    def test_dataset_query(self):
        """Test querying dataset"""
        parser = PulsePointDatasetParser(self.test_dir)
        # Test bounding box filtering
        results = parser.query_incidents("-118.3,34.0,-118.2,34.1")
        self.assertEqual(len(results), 2)
        
    def test_ingestor_dataset_mode(self):
        """Test PulsePointIngestor in dataset mode"""
        ingestor = PulsePointIngestor(dataset_path=self.test_dir)
        result = ingestor.ingest("-118.3,34.0,-118.2,34.1")
        self.assertEqual(len(result['data']), 2)
        self.assertEqual(result['source'], 'pulsepoint_dataset')

if __name__ == "__main__":
    unittest.main()
