from typing import List, Union
from energy_flexibility_kpis.kpi.base import KPI

class CapacityOfADR(KPI):
    """The amount of energy that can be added to or removed from the storage system during an ADR 
    action (up/down-flex)."""

    def __init__(*args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def calculate(self) -> Union[float, List[float]]:
        _ = super().calculate()
        raise NotImplementedError
    
class EnergyEfficiencyOfDemandResponseAction(KPI):
    """The fraction of the energy stored during the ADR event that can be used subsequently to reduce 
    the power needed to maintain thermal comfort."""

    def __init__(*args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def calculate(self) -> Union[float, List[float]]:
        _ = super().calculate()
        raise NotImplementedError
    
class AvailableFlexibleEnergy(KPI):
    """Amount of (thermal) energy stored in a building system (indoor environment and/or storage tank) 
    that can be used for load shifting."""

    def __init__(*args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def calculate(self) -> Union[float, List[float]]:
        _ = super().calculate()
        raise NotImplementedError