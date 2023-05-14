from typing import List, Union
from energy_flexibility_kpis.kpi.base import KPI

class RelativeCO2EmissionsReduction(KPI):
    """CO2 emissions savings due to the demand response of the building."""

    def __init__(*args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def calculate(self) -> Union[float, List[float]]:
        _ = super().calculate()
        raise NotImplementedError
    
class EnvironmentalSavings(KPI):
    """CO2 emissions savings due to the demand response of the building."""

    def __init__(*args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def calculate(self) -> Union[float, List[float]]:
        _ = super().calculate()
        raise NotImplementedError