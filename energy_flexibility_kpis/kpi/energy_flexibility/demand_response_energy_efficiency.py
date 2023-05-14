from typing import List, Union
from energy_flexibility_kpis.kpi.base import KPI

class EnergySavingsOfDemandResponse(KPI):
    """Difference between reference energy usage without demand response and and the energy 
    usage with demand response over the next 24h."""

    def __init__(*args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def calculate(self) -> Union[float, List[float]]:
        _ = super().calculate()
        raise NotImplementedError
    
class EnergyConsumptionRatio(KPI):
    """Change in the total energy consumption when implementing an energy flexibility control strategy."""

    def __init__(*args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def calculate(self) -> Union[float, List[float]]:
        _ = super().calculate()
        raise NotImplementedError
    
class DemandRecoveryRatio(KPI):
    """Ratio between the observed electric energy use by the flexible electric heating systems 
    and the minimum electric energy use of those heating systems, quantifying the increase in 
    energy use due to load shifting. When the heating systems do not interact with the 
    electricity generation system, an optimisation towards minimum electrical energy use is 
    performed at the demand side. The DRR will therefore always be greater than or equal to 1."""

    def __init__(*args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def calculate(self) -> Union[float, List[float]]:
        _ = super().calculate()
        raise NotImplementedError
    
class ConsistencyWithEnergySavings(KPI):
    """This index compares the energy reduction in the optimized and most energy efficient scenario, respectively."""

    def __init__(*args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def calculate(self) -> Union[float, List[float]]:
        _ = super().calculate()
        raise NotImplementedError