from typing import List, Union
from energy_flexibility_kpis.kpi.base import KPI

class DeviationDecreaseFromTheFlatDemandProfile(KPI):
    """This index evaluate the ability of lighting power flexibility in the modification of 
    a building demand profile focusing on the variance of the demand profile (y values)."""

    def __init__(*args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def calculate(self) -> Union[float, List[float]]:
        _ = super().calculate()
        raise NotImplementedError

class FlexibilityMap(KPI):
    """Flexibility map (upward and downward load profile for the next 24h). Calculated 
    by MPC with black box model of the building and energy price forecast."""

    def __init__(*args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def calculate(self) -> Union[float, List[float]]:
        _ = super().calculate()
        raise NotImplementedError
    
class Ramp(KPI):
    """Ramp of the power consumption."""

    def __init__(*args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def calculate(self) -> Union[float, List[float]]:
        _ = super().calculate()
        raise NotImplementedError