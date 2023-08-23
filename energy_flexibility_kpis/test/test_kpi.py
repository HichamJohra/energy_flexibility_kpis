import unittest
import pandas as pd
import os

# import kpi functions
from energy_flexibility_kpis import kpi

class test_kpi(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.data1_simple = pd.read_csv(os.path.join(os.path.dirname(__file__), 'data1_simple.csv'))
        cls.timestamps1 = cls.data1_simple['timestamp'].tolist()
        cls.baseline_power1 = cls.data1_simple['baseline_power'].tolist()
        cls.flexible_power1 = cls.data1_simple['flexible_power'].tolist()

# test peak_power_reduction   
    def test_peak_power_reduction(self):
        # peak timestamps
        peak_timestamps = self.timestamps1[13]
        # call the function
        result = kpi.peak_power_reduction(peak_timestamps,self.baseline_power1,self.flexible_power1,self.timestamps1)
        # expected output
        expected_result = 2000
        # assert that the function return the expected output
        print("----------")
        print("peak_power_reduction test")
        print("Result:", result)
        print("Expected result:", expected_result)
        self.assertEqual(result, expected_result)          

# test flexibility_factor
    def test_flexibility_factor(self):
        # high price time frame 
        high_price_start_timestamp = "2022-01-01 13:00:00"
        high_price_end_timestamp = "2022-01-01 15:00:00"
        # call the function
        result = kpi.flexibility_factor(self.baseline_power1, high_price_start_timestamp, high_price_end_timestamp, self.timestamps1)
        # expected output
        expected_result = 0.394230769
        # assert that the function return the expected output
        print("----------")
        print("flexibility_factor test 1")
        print("Result:", result)
        print("Expected result:", expected_result)
        self.assertAlmostEqual(result, expected_result,places=9)    
        # call the function
        result = kpi.flexibility_factor(self.flexible_power1, high_price_start_timestamp, high_price_end_timestamp, self.timestamps1)
        # expected output
        expected_result = 0.482474227
        # assert that the function return the expected output
        print("----------")
        print("flexibility_factor test 2")
        print("Result:", result)
        print("Expected result:", expected_result)
        self.assertAlmostEqual(result, expected_result,places=9)        
        
# test load factor 
    def test_load_factor(self):
        # peak timestamps
        peak_timestamps = self.timestamps1[13]
        # call the function
        result = kpi.load_factor(self.baseline_power1,peak_timestamps,self.timestamps1)
        # expected output
        expected_result = 0.4333
        # assert that the function return the expected output
        print("----------")
        print("load_factor test 1")
        print("Result:", result)
        print("Expected result:", expected_result)
        self.assertAlmostEqual(result, expected_result,places=4)  
        # call the function
        result = kpi.load_factor(self.flexible_power1,peak_timestamps,self.timestamps1)
        # expected output
        expected_result = 0.505208333
        # assert that the function return the expected output
        print("----------")
        print("load_factor test 2")
        print("Result:", result)
        print("Expected result:", expected_result)
        self.assertAlmostEqual(result, expected_result,places=9)  
        
 # test building_energy_flexibility_index   
    def test_building_energy_flexibility_index(self):
        # select power for a evaluation window
        baseline_power = self.baseline_power1[13:16]
        flexible_power = self.flexible_power1[13:16]
        # call the function
        result = kpi.building_energy_flexibility_index(baseline_power,flexible_power)
        # expected output
        expected_result = 2133.3333
        # assert that the function return the expected output
        print("----------")
        print("building_energy_flexibility_index test")
        print("Result:", result)
        print("Expected result:", expected_result)
        self.assertAlmostEqual(result, expected_result,places=4)           
        
if __name__ == '__main__':
    unittest.main()
