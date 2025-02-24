import unittest
from havinosh_data_loader.process_csv import process_csv

class TestCSVProcessing(unittest.TestCase):
    def test_process_csv(self):
        """Basic test for CSV processing"""
        process_csv("test_csvs")  # Test folder with sample CSVs
        self.assertTrue(True)  # Just check if function runs without error

if __name__ == "__main__":
    unittest.main()
