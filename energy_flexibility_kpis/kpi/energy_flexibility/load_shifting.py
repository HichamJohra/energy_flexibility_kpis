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
        generic_electric_power_profile: List[float],
        high_price_start_timestamp: Union[int,datetime.datetime, str],
        high_price_end_timestamp: Union[int,datetime.datetime, str],
        timestamps: Union[List[int], List[datetime.datetime], List[str]],
        evaluation_start_timestamp: Union[int, datetime.datetime, str] = None,
        evaluation_end_timestamp: Union[int, datetime.datetime, str] = None,
    ) -> float:
        _, vs = super().calculate(
            generic_electric_power_profile=generic_electric_power_profile,
            high_price_start_timestamp=high_price_start_timestamp,
            high_price_end_timestamp=high_price_end_timestamp,
            timestamps=timestamps,
            evaluation_start_timestamp=evaluation_start_timestamp,
            evaluation_end_timestamp=evaluation_end_timestamp,
        )
        high_price_mask = vs.evaluation_mask & (vs.timestamps.value >= vs.high_price_start_timestamp.value) & (vs.timestamps.value <= vs.high_price_end_timestamp.value)
        low_price_mask = vs.evaluation_mask & (~high_price_mask)
        low_price_value = vs.generic_electric_power_profile.value[low_price_mask].mean()*len(low_price_mask)
        high_price_value = vs.generic_electric_power_profile[high_price_mask].mean()*len(high_price_mask)
        value = (low_price_value - high_price_value)/(low_price_value + high_price_value)

        return value
    
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
        generic_electric_power_profile: List[float],
        high_price_start_timestamp: Union[int,datetime.datetime, str],
        high_price_end_timestamp: Union[int,datetime.datetime, str],
        timestamps: Union[List[int], List[datetime.datetime], List[str]],
        evaluation_start_timestamp: Union[int, datetime.datetime, str] = None,
        evaluation_end_timestamp: Union[int, datetime.datetime, str] = None,
    ) -> float:
        _, vs = super().calculate(
            generic_electric_power_profile=generic_electric_power_profile,
            high_price_start_timestamp=high_price_start_timestamp,
            high_price_end_timestamp=high_price_end_timestamp,
            timestamps=timestamps,
            evaluation_start_timestamp=evaluation_start_timestamp,
            evaluation_end_timestamp=evaluation_end_timestamp,
        )
        high_price_mask = vs.evaluation_mask & (vs.timestamps.value >= vs.high_price_start_timestamp.value) & (vs.timestamps.value <= vs.high_price_end_timestamp.value)
        low_price_mask = vs.evaluation_mask & (~high_price_mask)
        low_price_value = vs.generic_electric_power_profile.value[low_price_mask].mean()*len(low_price_mask)
        high_price_value = vs.generic_electric_power_profile[high_price_mask].mean()*len(high_price_mask)
        value = (low_price_value - high_price_value)/(low_price_value + high_price_value)

        return value
    
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
        baseline_electric_energy_profile: List[float],
        flexible_electric_energy_profile: List[float],
        medium_generic_signal_start_timestamp: Union[List[int], List[datetime.datetime], List[str]],
        medium_generic_signal_end_timestamp: Union[List[int], List[datetime.datetime], List[str]],
        high_generic_signal_start_timestamp: Union[List[int], List[datetime.datetime], List[str]],
        high_generic_signal_end_timestamp: Union[List[int], List[datetime.datetime], List[str]],
        timestamps: Union[List[int], List[datetime.datetime], List[str]],
        evaluation_start_timestamp: Union[int, datetime.datetime, str] = None,
        evaluation_end_timestamp: Union[int, datetime.datetime, str] = None,
    ) -> float:
        _, vs = super().calculate(
            baseline_electric_energy_profile=baseline_electric_energy_profile,
            flexible_electric_energy_profile=flexible_electric_energy_profile,
            medium_generic_signal_start_timestamp=medium_generic_signal_start_timestamp,
            medium_generic_signal_end_timestamp=medium_generic_signal_end_timestamp,
            high_generic_signal_start_timestamp=high_generic_signal_start_timestamp,
            high_generic_signal_end_timestamp=high_generic_signal_end_timestamp,
            timestamps=timestamps,
            evaluation_start_timestamp=evaluation_start_timestamp,
            evaluation_end_timestamp=evaluation_end_timestamp,
        )

        medium_mask = vs.evaluation_mask & (vs.timestamps.value >= vs.medium_generic_signal_start_timestamp.value) & (vs.timestamps.value <= vs.medium_generic_signal_end_timestamp.value)
        high_mask = vs.evaluation_mask & (vs.timestamps.value >= vs.high_generic_signal_start_timestamp.value) & (vs.timestamps.value <= vs.high_generic_signal_end_timestamp.value)
        baseline_total_value = vs.baseline_electric_energy_profile.value[vs.evaluation_mask].sum()
        flexible_total_value = vs.flexible_electric_energy_profile.value[vs.evaluation_mask].sum()
        baseline_medium_value = vs.baseline_electric_energy_profile.value[medium_mask].sum()/baseline_total_value
        baseline_high_value = vs.baseline_electric_energy_profile.value[high_mask].sum()/baseline_total_value
        flexible_medium_value = vs.flexible_electric_energy_profile.value[medium_mask].sum()/flexible_total_value
        flexible_high_value = vs.flexible_electric_energy_profile.value[high_mask].sum()/flexible_total_value
        value = (
            (1 - (flexible_high_value/baseline_high_value)) 
            + (1 - (flexible_medium_value/baseline_medium_value))
        )*100.0/2.0
        
        return value
    
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
        
        raise NotImplementedError('Complex equation')
    
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
    DOE_FLEXIBILITY_CATEGORY = [DOEFlexibilityCategory.LOAD_SHIFTING, DOEFlexibilityCategory.LOAD_SHEDDING, DOEFlexibilityCategory.MODULATING]
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
        
        raise NotImplementedError('Complex equation')
    
class CyclePowerFlexibility(KPI):
    """The value for the average power that can be delivered as flexibility to the electrical 
    grid can be calculated. The following equations show the approach to calculate the average 
    power for each charging (forced) and discharging (delayed) process. The flexibility 
    factor is defined as the ability to shift the energy use from high to low price periods 
    and vice versa."""

    NAME = 'cycle power flexibility'
    DEFINITION = __doc__
    UNIT = Unit(numerator=[BaseUnit.KW])
    CATEGORY = KPICategory.EF_LOAD_SHIFTING
    RELEVANCE = Relevance.HIGH
    STAKEHOLDERS = [Stakeholder.GRID_OPERATOR, Stakeholder.TRANSMISSION_SYSTEM_OPERATOR, Stakeholder.DISTRIBUTION_SYSTEM_OPERATOR]
    COMPLEXITY = Complexity.MEDIUM
    NEED_BASELINE = False
    TEMPORAL_EVALUATION_WINDOW = TemporalEvaluationWindow.SINGLE_EVENT
    TEMPORAL_RESOLUTION = TemporalResolution.UNSPECIFIED
    SPATIAL_RESOLUTION = SpatialResolution.UNSPECIFIED
    DOE_FLEXIBILITY_CATEGORY = [DOEFlexibilityCategory.LOAD_SHEDDING]
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
        
        raise NotImplementedError('Complex equation')