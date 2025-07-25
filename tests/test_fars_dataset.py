"""Tests for FARS dataset integration"""
import os
import tempfile
import csv
import shutil
import unittest

from pre911.core.nhtsa_ingestor import NHTSAIngestor
from pre911.core.fars_dataset import FARSDataset

class TestFARSDatasetIntegration(unittest.TestCase):
    """Tests for FARS dataset integration"""
    
    @classmethod
    def setUpClass(cls):
        # Create a temporary test dataset directory
        cls.test_dir = tempfile.mkdtemp()
        cls.test_file = os.path.join(cls.test_dir, 'FARS2023_National.csv')
        
        # Create a sample FARS dataset file
        with open(cls.test_file, 'w') as f:
            writer = csv.writer(f)
            writer.writerow(['STATE', 'ST_CASE', 'YEAR', 'MONTH', 'DAY', 'HOUR', 'MINUTE', 
                            'LATITUDE', 'LONGITUD', 'FATALS', 'VE_TOTAL'])
            writer.writerow([6, '12345', 2023, 1, 15, 8, 30, 34.0522, -118.2437, 1, 2])
            writer.writerow([6, '12346', 2023, 2, 20, 14, 15, 34.0522, -118.2437, 2, 1])
            writer.writerow([8, '12347', 2023, 3, 10, 12, 0, 39.7392, -104.9903, 1, 3])
    
    @classmethod
    def tearDownClass(cls):
        # Clean up test directory
        shutil.rmtree(cls.test_dir)
    
    def test_dataset_loading(self):
        """Test loading FARS dataset files"""
        dataset = FARSDataset(self.test_dir)
        self.assertTrue(dataset.load(2023))
        self.assertEqual(len(dataset.data), 3)
        
    def test_ingestor_dataset_mode(self):
        """Test NHTSAIngestor in dataset mode"""
        ingestor = NHTSAIngestor(data_dir=self.test_dir)
        result = ingestor.get_case_list(states=[6], from_year=2023, to_year=2023)
        self.assertEqual(len(result['data']), 2)
        self.assertEqual(result['source'], 'fars_dataset')

if __name__ == "__main__":
    unittest.main()
