import datetime
from typing import List, Union
from energy_flexibility_kpis.kpi.base import KPI
from energy_flexibility_kpis.enumerations import BaseUnit, Complexity, DOEFlexibilityCategory, KPICategory, PerformanceAspect, Relevance 
from energy_flexibility_kpis.enumerations import Stakeholder, TemporalEvaluationWindow,TemporalResolution, SpatialResolution
from energy_flexibility_kpis.unit import Unit

class EnergyShiftFlexibilityFactor(KPI):
    """Measures the capability for shifting the energy consumption between periods: in here 
    from daytime to night time."""

    NAME = 'energy shift flexibility factor'
    DEFINITION = __doc__
    UNIT = Unit(numerator=[BaseUnit.DIMENSIONLESS])
    CATEGORY = KPICategory.EF_LOAD_SHIFTING
    RELEVANCE = Relevance.HIGH
    STAKEHOLDERS = [Stakeholder.DISTRIBUTION_SYSTEM_OPERATOR, Stakeholder.TRANSMISSION_SYSTEM_OPERATOR, Stakeholder.BUILDING_OWNER]
    COMPLEXITY = Complexity.LOW
    NEED_BASELINE = False
    TEMPORAL_EVALUATION_WINDOW = TemporalEvaluationWindow.UNSPECIFIED
    TEMPORAL_RESOLUTION = TemporalResolution.UNSPECIFIED
    SPATIAL_RESOLUTION = SpatialResolution.UNSPECIFIED
    DOE_FLEXIBILITY_CATEGORY = [DOEFlexibilityCategory.LOAD_SHIFTING]
    PERFORMANCE_ASPECT = [PerformanceAspect.ENERGY]

    def __init__(self):
        super().__init__()

    @classmethod
    def calculate(
        cls,
        timestamps: Union[List[int], List[datetime.datetime], List[str]] = None,
        evaluation_start_timestamp: Union[int, datetime.datetime, str] = None,
        evaluation_end_timestamp: Union[int, datetime.datetime, str] = None,
    ) -> float:
        _, vs = super().calculate(
            timestamps=timestamps,
            evaluation_start_timestamp=evaluation_start_timestamp,
            evaluation_end_timestamp=evaluation_end_timestamp,
        )
        
        raise NotImplementedError
    
class FlexibilityFactor(KPI):
    """Ability to shift a quantity (e.g., energy, cost, emissions) from high-load periods to 
    low-load periods. It ranges between -1 (quantify was only during high-load periods) and 1 
    (quantify was only during low-load periods)."""
    
    NAME = 'flexibility factor'
    DEFINITION = __doc__
    UNIT = Unit(numerator=[BaseUnit.DIMENSIONLESS])
    CATEGORY = KPICategory.EF_LOAD_SHIFTING
    RELEVANCE = Relevance.HIGH
    STAKEHOLDERS = [Stakeholder.DISTRIBUTION_SYSTEM_OPERATOR, Stakeholder.TRANSMISSION_SYSTEM_OPERATOR, Stakeholder.BUILDING_OWNER]
    COMPLEXITY = Complexity.LOW
    NEED_BASELINE = False
    TEMPORAL_EVALUATION_WINDOW = TemporalEvaluationWindow.UNSPECIFIED
    TEMPORAL_RESOLUTION = TemporalResolution.UNSPECIFIED
    SPATIAL_RESOLUTION = SpatialResolution.UNSPECIFIED
    DOE_FLEXIBILITY_CATEGORY = [DOEFlexibilityCategory.LOAD_SHIFTING]
    PERFORMANCE_ASPECT = [PerformanceAspect.ENERGY, PerformanceAspect.COST, PerformanceAspect.EMISSION]

    def __init__(self):
        super().__init__()

    @classmethod
    def calculate(
        cls,
        timestamps: Union[List[int], List[datetime.datetime], List[str]] = None,
        evaluation_start_timestamp: Union[int, datetime.datetime, str] = None,
        evaluation_end_timestamp: Union[int, datetime.datetime, str] = None,
    ) -> float:
        _, vs = super().calculate(
            timestamps=timestamps,
            evaluation_start_timestamp=evaluation_start_timestamp,
            evaluation_end_timestamp=evaluation_end_timestamp,
        )
        
        raise NotImplementedError
    
class FlexibilityIndex(KPI):
    """It represents the change of heating use during medium and high price periods when the 
    energy is accumulated during low price periods compared to a reference scenario without 
    any demand response strategy. High, medium and low price periods can be defined with 
    percentiles of the last 2 weeks of energy spot price. If there is no remaining energy 
    usage during the periods of high and medium price, the flexibility index takes the maximum 
    value of 100%."""
    
    NAME = 'flexibility index'
    DEFINITION = __doc__
    UNIT = Unit(numerator=[BaseUnit.PERCENT])
    CATEGORY = KPICategory.EF_LOAD_SHIFTING
    RELEVANCE = Relevance.HIGH
    STAKEHOLDERS = [Stakeholder.GRID_OPERATOR, Stakeholder.BUILDING_OWNER]
    COMPLEXITY = Complexity.LOW
    NEED_BASELINE = True
    TEMPORAL_EVALUATION_WINDOW = TemporalEvaluationWindow.WHOLE_YEAR
    TEMPORAL_RESOLUTION = TemporalResolution.UNSPECIFIED
    SPATIAL_RESOLUTION = SpatialResolution.UNSPECIFIED
    DOE_FLEXIBILITY_CATEGORY = [DOEFlexibilityCategory.LOAD_SHIFTING]
    PERFORMANCE_ASPECT = [PerformanceAspect.ENERGY]

    def __init__(self):
        super().__init__()

    @classmethod
    def calculate(
        cls,
        timestamps: Union[List[int], List[datetime.datetime], List[str]] = None,
        evaluation_start_timestamp: Union[int, datetime.datetime, str] = None,
        evaluation_end_timestamp: Union[int, datetime.datetime, str] = None,
    ) -> float:
        _, vs = super().calculate(
            timestamps=timestamps,
            evaluation_start_timestamp=evaluation_start_timestamp,
            evaluation_end_timestamp=evaluation_end_timestamp,
        )
        
        raise NotImplementedError
    
class FlexibilityClassificationFactor(KPI):
    """Green signals indicate low prices (class A/B) and yellow/red indicate high prices 
    (class C/D). FCF is 100% (=1) when all energy costs are in classes A and B. This 
    corresponds with a high use of flexibility and a depleted flexibility potential. 
    FC is 0% (=0) when all energy costs are in classes C and D. In this case, unused 
    flexibility potential is available. The higher the flexibility of a building, 
    the higher the FCF value."""
    
    NAME = 'flexibility classification factor'
    DEFINITION = __doc__
    UNIT = Unit(numerator=[BaseUnit.DIMENSIONLESS])
    CATEGORY = KPICategory.EF_LOAD_SHIFTING
    RELEVANCE = Relevance.HIGH
    STAKEHOLDERS = [Stakeholder.POLICYMAKER, Stakeholder.TRANSMISSION_SYSTEM_OPERATOR, Stakeholder.DISTRIBUTION_SYSTEM_OPERATOR]
    COMPLEXITY = Complexity.MEDIUM
    NEED_BASELINE = False
    TEMPORAL_EVALUATION_WINDOW = TemporalEvaluationWindow.WHOLE_YEAR
    TEMPORAL_RESOLUTION = TemporalResolution.UNSPECIFIED
    SPATIAL_RESOLUTION = SpatialResolution.UNSPECIFIED
    DOE_FLEXIBILITY_CATEGORY = [DOEFlexibilityCategory.LOAD_SHIFTING]
    PERFORMANCE_ASPECT = [PerformanceAspect.COST, PerformanceAspect.EMISSION]

    def __init__(self):
        super().__init__()

    @classmethod
    def calculate(
        cls,
        timestamps: Union[List[int], List[datetime.datetime], List[str]] = None,
        evaluation_start_timestamp: Union[int, datetime.datetime, str] = None,
        evaluation_end_timestamp: Union[int, datetime.datetime, str] = None,
    ) -> float:
        _, vs = super().calculate(
            timestamps=timestamps,
            evaluation_start_timestamp=evaluation_start_timestamp,
            evaluation_end_timestamp=evaluation_end_timestamp,
        )
        
        raise NotImplementedError
    
class FlexibilityIndicator(KPI):
    """How much shape modification from reference energy profile to the target profile 
    in the next 24h: evaluation of the energy profile time series distance to reference 
    profile and target profile. Requires optimization."""
    
    NAME = 'flexibility indicator'
    DEFINITION = __doc__
    UNIT = Unit(numerator=[BaseUnit.DIMENSIONLESS])
    CATEGORY = KPICategory.EF_LOAD_SHIFTING
    RELEVANCE = Relevance.HIGH
    STAKEHOLDERS = [Stakeholder.BUILDING_OWNER, Stakeholder.OCCUPANT, Stakeholder.BUILDING_MANAGER, Stakeholder.AGGREGATOR, Stakeholder.GRID_OPERATOR]
    COMPLEXITY = Complexity.HIGH
    NEED_BASELINE = True
    TEMPORAL_EVALUATION_WINDOW = TemporalEvaluationWindow.WHOLE_DAY
    TEMPORAL_RESOLUTION = TemporalResolution.HOURLY
    SPATIAL_RESOLUTION = SpatialResolution.SINGLE_BUILDING
    DOE_FLEXIBILITY_CATEGORY = [DOEFlexibilityCategory.LOAD_SHIFTING]
    PERFORMANCE_ASPECT = [PerformanceAspect.ENERGY]

    def __init__(self):
        super().__init__()

    @classmethod
    def calculate(
        cls,
        timestamps: Union[List[int], List[datetime.datetime], List[str]] = None,
        evaluation_start_timestamp: Union[int, datetime.datetime, str] = None,
        evaluation_end_timestamp: Union[int, datetime.datetime, str] = None,
    ) -> float:
        _, vs = super().calculate(
            timestamps=timestamps,
            evaluation_start_timestamp=evaluation_start_timestamp,
            evaluation_end_timestamp=evaluation_end_timestamp,
        )
        
        raise NotImplementedError
    
class CyclePowerFlexibility(KPI):
    """The value for the average power that can be delivered as flexibility to the electrical 
    grid can be calculated. The following equations show the approach to calculate the average 
    power for each charging (forced) and discharging (delayed) process. The flexibility 
    factor is defined as the ability to shift the energy use from high to low price periods 
    and viceversa."""
    
    NAME = 'cycle power flexibility'
    DEFINITION = __doc__
    UNIT = Unit(numerator=[BaseUnit.KW])
    CATEGORY = KPICategory.EF_LOAD_SHIFTING
    RELEVANCE = Relevance.HIGH
    STAKEHOLDERS = [Stakeholder.GRID_OPERATOR, Stakeholder.DISTRIBUTION_SYSTEM_OPERATOR, Stakeholder.TRANSMISSION_SYSTEM_OPERATOR]
    COMPLEXITY = Complexity.MEDIUM
    NEED_BASELINE = False
    TEMPORAL_EVALUATION_WINDOW = TemporalEvaluationWindow.SINGLE_EVENT
    TEMPORAL_RESOLUTION = TemporalResolution.UNSPECIFIED
    SPATIAL_RESOLUTION = SpatialResolution.UNSPECIFIED
    DOE_FLEXIBILITY_CATEGORY = [DOEFlexibilityCategory.LOAD_SHIFTING]
    PERFORMANCE_ASPECT = [PerformanceAspect.POWER]

    def __init__(self):
        super().__init__()

    @classmethod
    def calculate(
        cls,
        timestamps: Union[List[int], List[datetime.datetime], List[str]] = None,
        evaluation_start_timestamp: Union[int, datetime.datetime, str] = None,
        evaluation_end_timestamp: Union[int, datetime.datetime, str] = None,
    ) -> float:
        _, vs = super().calculate(
            timestamps=timestamps,
            evaluation_start_timestamp=evaluation_start_timestamp,
            evaluation_end_timestamp=evaluation_end_timestamp,
        )
        
        raise NotImplementedError