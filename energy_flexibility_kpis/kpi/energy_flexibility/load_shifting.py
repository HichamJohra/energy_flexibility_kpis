from typing import List, Union
from energy_flexibility_kpis.kpi.base import KPI

class EnergyShiftFlexibilityFactor(KPI):
    """Measures the capability for shifting the energy consumption between periods: in here 
    from daytime to night time."""

    def __init__(*args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def calculate(self) -> Union[float, List[float]]:
        _ = super().calculate()
        raise NotImplementedError
    
class FlexibilityFactor(KPI):
    """Ability to shift a quantity (e.g., energy, cost, emissions) from high-load periods to 
    low-load periods. It ranges between -1 (quantify was only during high-load periods) and 1 
    (quantify was only during low-load periods)."""

    def __init__(*args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def calculate(self) -> Union[float, List[float]]:
        _ = super().calculate()
        raise NotImplementedError
    
class FlexibilityIndex(KPI):
    """It represents the change of heating use during medium and high price periods when the 
    energy is accumulated during low price periods compared to a reference scenario without 
    any demand response strategy. High, medium and low price periods can be defined with 
    percentiles of the last 2 weeks of energy spot price. If there is no remaining energy 
    usage during the periods of high and medium price, the flexibility index takes the maximum 
    value of 100%."""

    def __init__(*args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def calculate(self) -> Union[float, List[float]]:
        _ = super().calculate()
        raise NotImplementedError
    
class FlexibilityClassificationFactor(KPI):
    """Green signals indicate low prices (class A/B) and yellow/red indicate high prices 
    (class C/D). FCF is 100% (=1) when all energy costs are in classes A and B. This 
    corresponds with a high use of flexibility and a depleted flexibility potential. 
    FC is 0% (=0) when all energy costs are in classes C and D. In this case, unused 
    flexibility potential is available. The higher the flexibility of a building, 
    the higher the FCF value."""

    def __init__(*args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def calculate(self) -> Union[float, List[float]]:
        _ = super().calculate()
        raise NotImplementedError
    
class FlexibilityIndicator(KPI):
    """How much shape modification from reference energy profile to the target profile 
    in the next 24h: evaluation of the energy profile time series distance to reference 
    profile and target profile. Requires optimization."""

    def __init__(*args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def calculate(self) -> Union[float, List[float]]:
        _ = super().calculate()
        raise NotImplementedError
    
class CyclePowerFlexibility(KPI):
    """The value for the average power that can be delivered as flexibility to the electrical 
    grid can be calculated. The following equations show the approach to calculate the average 
    power for each charging (forced) and discharging (delayed) process. The flexibility 
    factor is defined as the ability to shift the energy use from high to low price periods 
    and viceversa."""

    def __init__(*args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def calculate(self) -> Union[float, List[float]]:
        _ = super().calculate()
        raise NotImplementedError