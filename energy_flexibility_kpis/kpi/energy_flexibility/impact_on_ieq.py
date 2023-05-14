from typing import List, Union
from energy_flexibility_kpis.kpi.base import KPI

class CumulativeAverageThermalDiscomfort(KPI):
    """Defines the cumulative deviation of zone temperatures from upper and 
    lower comfort limits that are predefined within the test case FMU for 
    each zone, averaged over all zones."""

    def __init__(*args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def calculate(self) -> Union[float, List[float]]:
        _ = super().calculate()
        raise NotImplementedError
    
class CumulativeAverageIndoorAirQualityDiscomfort(KPI):
    """Defines the extent that the CO2 concentration levels in zones exceed 
    bounds of the acceptable concentration level, which are predefined within 
    the test case FMU for each zone, averaged over all zones."""

    def __init__(*args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def calculate(self) -> Union[float, List[float]]:
        _ = super().calculate()
        raise NotImplementedError
    
class ImpactedDwellingsPercentage(KPI):
    """The percentage of the dwellings with a different duration of EHP activation 
    compared with the BaU case."""

    def __init__(*args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def calculate(self) -> Union[float, List[float]]:
        _ = super().calculate()
        raise NotImplementedError
    
class AverageDisruptionDuration(KPI):
    """Measure the average change of EHP activation time across the service deployment period."""

    def __init__(*args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def calculate(self) -> Union[float, List[float]]:
        _ = super().calculate()
        raise NotImplementedError