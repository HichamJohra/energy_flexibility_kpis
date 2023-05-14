from typing import List, Union
from energy_flexibility_kpis.kpi.base import KPI

class SelfConsumptionDuringDRAction(KPI):
    """The proportion of increased demand covered by onsite generation. This indicator 
    is a measure of the coincidence between locally produced electricity and increased 
    demand during a DR action."""

    def __init__(*args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def calculate(self) -> Union[float, List[float]]:
        _ = super().calculate()
        raise NotImplementedError
    
class RelativeEnergyImportSavings(KPI):
    """Energy import savings (reduction of the residual power demand that is not covered 
    by local RES production) during demand response period in comparison to the reference 
    operation."""

    def __init__(*args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def calculate(self) -> Union[float, List[float]]:
        _ = super().calculate()
        raise NotImplementedError
    
class FlexibilityAggregationSynergyFactor(KPI):
    """Quantify the benefit of aggregating multiple flexible systems by measuring the 
    amount of additional Secondary Frequency Regulation (SFR) capacity that is available 
    from the aggregation relative to the sum of SFR capacities the systems could 
    provide individually."""

    def __init__(*args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def calculate(self) -> Union[float, List[float]]:
        _ = super().calculate()
        raise NotImplementedError