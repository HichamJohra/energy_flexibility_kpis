from typing import List, Union
from energy_flexibility_kpis.kpi.base import KPI

class PeakPowerRebound(KPI):
    """Power demand increase during peak hour after flexible operation (rebound effect)."""

    def __init__(*args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def calculate(self) -> Union[float, List[float]]:
        _ = super().calculate()
        raise NotImplementedError
    
class AveragePowerRebound(KPI):
    """Average power rebound after DR event compared to baseline."""

    def __init__(*args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def calculate(self) -> Union[float, List[float]]:
        _ = super().calculate()
        raise NotImplementedError
    
class ReboundEnergy(KPI):
    """Size of consumption deviation prior / following an DR event. Important to grid 
    operation to ensure stability / balance outside DR period."""

    def __init__(*args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def calculate(self) -> Union[float, List[float]]:
        _ = super().calculate()
        raise NotImplementedError