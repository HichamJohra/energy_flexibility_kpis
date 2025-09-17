import unittest
from datetime import datetime
import energy_flexibility_kpis.kpi.energy_flexibility.energy_or_average_power_load_shedding as energy_or_average_power_load_shedding
import pandas as pd
import numpy as np
import os

# get the directory of the current file
dir_path = os.path.dirname(os.path.realpath(__file__))

class test_EnergyDeviationForPeakShaving(unittest.TestCase):

    def test_calculate(self):
        # given
        data = pd.read_csv(os.path.join(dir_path, 'data_24hr_hourly.csv'))
        baseline_electric_power_profile = data['baseline_power'].tolist()
        flexible_electric_power_profile = data['flexible_power'].tolist()
        timestamps = pd.to_datetime(data['timestamp']).tolist()
        evaluation_start_timestamp = datetime(2022, 1, 1, 13, 0)
        evaluation_end_timestamp = datetime(2022, 1, 1, 15, 0)

        # result
        result = energy_or_average_power_load_shedding.EnergyDeviationForPeakShaving().calculate(
            baseline_electric_power_profile = baseline_electric_power_profile,
            flexible_electric_power_profile = flexible_electric_power_profile,
            timestamps=timestamps,
            evaluation_start_timestamp = evaluation_start_timestamp,
            evaluation_end_timestamp = evaluation_end_timestamp
        )

        # expeted
        expected = 6400
        # for res, exp in zip(result, expected):
        self.assertAlmostEqual(result, expected, 3)

class test_AverageLoadReduction(unittest.TestCase):

    def test_calculate(self):
        # given
        data = pd.read_csv(os.path.join(dir_path, 'data_24hr_hourly.csv'))
        baseline_electric_power_profile = data['baseline_power'].tolist()
        flexible_electric_power_profile = data['flexible_power'].tolist()
        timestamps = pd.to_datetime(data['timestamp']).tolist()
        generic_signal_start_timestamp = datetime(2022, 1, 1, 13, 0)
        generic_signal_end_timestamp = datetime(2022, 1, 1, 15, 0)
        evaluation_start_timestamp = datetime(2022, 1, 1, 13, 0)
        evaluation_end_timestamp = datetime(2022, 1, 1, 15, 0)

        # result
        result = energy_or_average_power_load_shedding.AverageLoadReduction().calculate(
            baseline_electric_power_profile = baseline_electric_power_profile,
            flexible_electric_power_profile = flexible_electric_power_profile,
            generic_signal_start_timestamp = generic_signal_start_timestamp,
            generic_signal_end_timestamp = generic_signal_end_timestamp,
            timestamps=timestamps,
            evaluation_start_timestamp = evaluation_start_timestamp,
            evaluation_end_timestamp = evaluation_end_timestamp
        )

        # expected
        expected = 6400
        self.assertAlmostEqual(result, expected, 3)

# class test_AverageLoadReduction(unittest.TestCase):

#     def test_calculate(self):
#         # given
#         data = pd.read_csv('data_24hr_hourly.csv')
#         baseline_electric_power_profile = data['baseline_power'].tolist()
#         flexible_electric_power_profile = data['flexible_power'].tolist()
#         timestamps = pd.to_datetime(data['timestamp']).tolist()
#         evaluation_start_timestamp = datetime(2022, 1, 1, 13, 0)
#         evaluation_end_timestamp = datetime(2022, 1, 1, 15, 0)

#         # result
#         result = energy_or_average_power_load_shedding.AverageLoadReduction().calculate(
#             baseline_electric_power_profile = baseline_electric_power_profile,
#             flexible_electric_power_profile = flexible_electric_power_profile,
#             timestamps=timestamps,
#             evaluation_start_timestamp = evaluation_start_timestamp,
#             evaluation_end_timestamp = evaluation_end_timestamp
#         )

#         # expeted
#         expected = -6400
#         # for res, exp in zip(result, expected):
#         self.assertAlmostEqual(result, expected, 3)
    
# class test_BuildingEnergyFlexibilityIndex(unittest.TestCase):

#     def test_calculate(self):
#         # given
#         data = pd.read_csv(os.path.join(dir_path, 'data_24hr_hourly.csv'))
#         baseline_electric_power_profile = data['baseline_power'].tolist()
#         flexible_electric_power_profile = data['flexible_power'].tolist()
#         timestamps = pd.to_datetime(data['timestamp']).tolist()
#         evaluation_start_timestamp = datetime(2022, 1, 1, 13, 0)
#         evaluation_end_timestamp = datetime(2022, 1, 1, 15, 0)

#         # result
#         result = energy_or_average_power_load_shedding.BuildingEnergyFlexibilityIndex().calculate(
#             baseline_electric_power_profile = baseline_electric_power_profile,
#             flexible_electric_power_profile = flexible_electric_power_profile,
#             timestamps=timestamps,
#             evaluation_start_timestamp = evaluation_start_timestamp,
#             evaluation_end_timestamp = evaluation_end_timestamp
#         )

#         # expeted
#         expected = 2133.33
#         # for res, exp in zip(result, expected):
#         self.assertAlmostEqual(result, expected, 3)
        
# class test_PowerPaybackRatio(unittest.TestCase):


if __name__ == '__main__':
    unittest.main()
