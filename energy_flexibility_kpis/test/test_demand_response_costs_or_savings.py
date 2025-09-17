import unittest
from datetime import datetime
import numpy as np
from energy_flexibility_kpis.kpi.energy_flexibility.demand_response_costs_or_savings import (
    FlexibilitySavingsIndex,
    CostOrEnergyDeviationRatio,
    RelativeOperationalCostOfADR,
    CostSavings,
)

class test_CostOrEnergyDeviationRatio(unittest.TestCase):

    def test_calculate(self):
        baseline_electric_power_profile = [10, 20, 30]
        baseline_cost_profile = [100, 200, 300]
        flexible_electric_power_profile = [8, 18, 28]
        flexible_cost_profile = [80, 180, 280]
        timestamps = [datetime(2022, 1, 1), datetime(2022, 1, 2), datetime(2022, 1, 3)]
        expected_result = 10.0

        result = CostOrEnergyDeviationRatio.calculate(
            baseline_electric_power_profile,
            baseline_cost_profile,
            flexible_electric_power_profile,
            flexible_cost_profile,
            timestamps
        )

        self.assertEqual(result, expected_result)

class test_FlexibilitySavingsIndex(unittest.TestCase):

    def test_calculate(self):
        baseline_cost_profile = [100, 200, 300]
        flexible_cost_profile = [10, 20, 30]
        timestamps = [datetime(2022, 1, 1), datetime(2022, 1, 2), datetime(2022, 1, 3)]
        expected_result = 0.9

        result = FlexibilitySavingsIndex.calculate(
            baseline_cost_profile,
            flexible_cost_profile,
            timestamps
        )

        self.assertEqual(result, expected_result)

class test_RelativeOperationalCostOfADR(unittest.TestCase):

    def test_calculate(self):
        baseline_cost_profile = [100, 200, 300]
        flexible_cost_profile = [10, 20, 30]
        timestamps = [datetime(2022, 1, 1), datetime(2022, 1, 2), datetime(2022, 1, 3)]
        expected_result = 0.1

        result = RelativeOperationalCostOfADR.calculate(
            baseline_cost_profile,
            flexible_cost_profile,
            timestamps
        )

        self.assertEqual(result, expected_result)



if __name__ == '__main__':
    unittest.main()
