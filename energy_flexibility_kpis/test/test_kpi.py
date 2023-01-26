import unittest
import pandas as pd

# import kpi functions
import sys
import os
parent_directory = os.path.dirname(os.path.dirname(__file__))
sys.path.append(parent_directory)
import kpi

class test_kpi(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.data1_simple = pd.read_csv(os.path.join(os.path.dirname(__file__), 'data1_simple.csv'))
        cls.timestamps1_simple = cls.data1_simple['timestamp'].tolist()
        cls.baseline_power1_simple = cls.data1_simple['baseline_power'].tolist()
        cls.flexible_power1_simple = cls.data1_simple['flexible_power'].tolist()

    # test flexibility factor
    def test_flexibility_factor(self):
        # high price time frame 
        high_price_start_timestamp = "2022-01-01 13:00:00"
        high_price_end_timestamp = "2022-01-01 15:00:00"
        # call the function
        result = kpi.flexibility_factor(self.baseline_power1_simple, high_price_start_timestamp, high_price_end_timestamp, self.timestamps1_simple)
        # expected output
        expected_result = 0.394231
        # assert that the function return the expected output
        self.assertAlmostEqual(result, expected_result,places=6)    
        
if __name__ == '__main__':
    unittest.main()
