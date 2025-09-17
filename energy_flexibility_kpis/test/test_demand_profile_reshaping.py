import unittest
from datetime import datetime
import energy_flexibility_kpis.kpi.energy_flexibility.demand_profile_reshaping as demand_profile_reshaping
import pandas as pd
import numpy as np
import os

# get the directory of the current file
dir_path = os.path.dirname(os.path.realpath(__file__))

class test_DeviationDecreaseFromTheFlatDemandProfile(unittest.TestCase):

    def test_calculate(self):
        # given
        data = pd.read_csv(os.path.join(dir_path, 'data_24hr_hourly.csv'))
        baseline_electric_power_profile = data['baseline_power'].tolist()
        flexible_electric_power_profile = data['flexible_power'].tolist()

        # result
        result = demand_profile_reshaping.DeviationDecreaseFromTheFlatDemandProfile().calculate(
            baseline_electricity_consumption_profile = baseline_electric_power_profile,
            flexible_electricity_consumption_profile = flexible_electric_power_profile,
        )

        # expeted
        expected = 0.092
        
        # assert
        self.assertAlmostEqual(result, expected, 3)

class test_Ramp(unittest.TestCase):
    def setUp(self):
        self.ramp = demand_profile_reshaping.Ramp()

    def test_calculate_with_generic_electric_power_profile(self):
        # given
        generic_electric_power_profile = [10, 20, 35, 55, 80]

        # result
        result = self.ramp.calculate(generic_electric_power_profile)

        # expected
        expected = [np.nan, 10, 15, 20, 25]

        # assert
        self.assertTrue(np.isnan(result[0]))
        np.testing.assert_allclose(result[1:], expected[1:], rtol=1e-3)

if __name__ == '__main__':
    unittest.main()