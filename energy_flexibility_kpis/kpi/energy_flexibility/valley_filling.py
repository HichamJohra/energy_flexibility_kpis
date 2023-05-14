from typing import List, Union
from energy_flexibility_kpis.kpi.base import KPI

class EnergyDeviationForValleyFilling(KPI):
    """Valley-filling capacity."""

    def __init__(*args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def calculate(self) -> Union[float, List[float]]:
        _ = super().calculate()
        raise NotImplementedError
    
class AveragePowerDeviation(KPI):
    """Average power deviation (DP)."""

    def __init__(*args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def calculate(self) -> Union[float, List[float]]:
        _ = super().calculate()
        raise NotImplementedError