import datetime
from typing import List, Union
from scipy import integrate
from energy_flexibility_kpis.kpi.base import KPI
from energy_flexibility_kpis.enumerations import BaseUnit, Complexity, DOEFlexibilityCategory, KPICategory, PerformanceAspect, Relevance 
from energy_flexibility_kpis.enumerations import Stakeholder, TemporalEvaluationWindow,TemporalResolution, SpatialResolution
from energy_flexibility_kpis.unit import Unit

class FlexibilitySavingsIndex(KPI):
    """The fraction of saved cost from a penalty-aware operational strategy (flexible) 
    compared with a penalty-ignorant operation strategy (baseline)."""

    NAME = 'flexibility savings index'
    DEFINITION = __doc__
    UNIT = Unit(numerator=[BaseUnit.DIMENSIONLESS])
    CATEGORY = KPICategory.EF_DEMAND_RESPONSE_COSTS_OR_SAVINGS
    RELEVANCE = Relevance.HIGH
    STAKEHOLDERS = [Stakeholder.BUILDING_OPERATOR, Stakeholder.BUILDING_OWNER]
    COMPLEXITY = Complexity.LOW
    NEED_BASELINE = True
    TEMPORAL_EVALUATION_WINDOW = TemporalEvaluationWindow.UNSPECIFIED
    TEMPORAL_RESOLUTION = TemporalResolution.UNSPECIFIED
    SPATIAL_RESOLUTION = SpatialResolution.UNSPECIFIED
    DOE_FLEXIBILITY_CATEGORY = [DOEFlexibilityCategory.EFFICIENCY, DOEFlexibilityCategory.LOAD_SHEDDING, DOEFlexibilityCategory.LOAD_SHIFTING]
    PERFORMANCE_ASPECT = [PerformanceAspect.COST]

    def __init__(self):
        super().__init__()

    @classmethod
    def calculate(
        cls,
        baseline_cost_profile: List[float],
        flexible_cost_profile: List[float],
        timestamps: Union[List[int], List[datetime.datetime], List[str]] = None,
        evaluation_start_timestamp: Union[int, datetime.datetime, str] = None,
        evaluation_end_timestamp: Union[int, datetime.datetime, str] = None,
    ) -> List[float]:
        _, vs = super().calculate(
            baseline_cost_profile=baseline_cost_profile,
            flexible_cost_profile=flexible_cost_profile,
            timestamps=timestamps,
            evaluation_start_timestamp=evaluation_start_timestamp,
            evaluation_end_timestamp=evaluation_end_timestamp,
        )
        
        value = 1 - (vs.flexible_cost_profile.value[vs.evaluation_mask].sum()/vs.baseline_cost_profile.value[vs.evaluation_mask].sum())

        return value
    
class CostOrEnergyDeviationRatio(KPI):
    """Flexibility is assessed by the energy consumption and cost deviations resulting from 
    DR measures with respect a reference scenario without DR."""

    NAME = 'cost or energy deviation ratio'
    DEFINITION = __doc__
    UNIT = Unit(numerator=[BaseUnit.PERCENT])
    CATEGORY = KPICategory.EF_DEMAND_RESPONSE_COSTS_OR_SAVINGS
    RELEVANCE = Relevance.HIGH
    STAKEHOLDERS = [Stakeholder.BUILDING_OPERATOR, Stakeholder.BUILDING_OWNER]
    COMPLEXITY = Complexity.LOW
    NEED_BASELINE = True
    TEMPORAL_EVALUATION_WINDOW = TemporalEvaluationWindow.WHOLE_YEAR
    TEMPORAL_RESOLUTION = TemporalResolution.UNSPECIFIED
    SPATIAL_RESOLUTION = SpatialResolution.BUILDING_CLUSTER
    DOE_FLEXIBILITY_CATEGORY = [DOEFlexibilityCategory.LOAD_SHEDDING, DOEFlexibilityCategory.LOAD_SHIFTING, DOEFlexibilityCategory.GENERATION]
    PERFORMANCE_ASPECT = [PerformanceAspect.COST]

    def __init__(self):
        super().__init__()

    @classmethod
    def calculate(
        cls,
        baseline_electric_power_profile: List[float],
        baseline_cost_profile: List[float],
        flexible_electric_power_profile: List[float],
        flexible_cost_profile: List[float],
        timestamps: Union[List[int], List[datetime.datetime], List[str]],
        evaluation_start_timestamp: Union[int, datetime.datetime, str] = None,
        evaluation_end_timestamp: Union[int, datetime.datetime, str] = None,
    ) -> float:
        _, vs = super().calculate(
            baseline_electric_power_profile=baseline_electric_power_profile,
            baseline_cost_profile=baseline_cost_profile,
            flexible_electric_power_profile=flexible_electric_power_profile,
            flexible_cost_profile=flexible_cost_profile,
            timestamps=timestamps,
            evaluation_start_timestamp=evaluation_start_timestamp,
            evaluation_end_timestamp=evaluation_end_timestamp,
        )
        
        dx = vs.get_temporal_resolution(BaseUnit.HOUR, value=vs.timestamps.value[vs.evaluation_mask])
        cost_profile = vs.flexible_cost_profile.value[vs.evaluation_mask] - vs.baseline_cost_profile.value[vs.evaluation_mask]
        electric_power_profile = vs.flexible_electric_power_profile.value[vs.evaluation_mask] - vs.baseline_electric_power_profile.value[vs.evaluation_mask]
        cost_value = integrate.simpson(cost_profile, dx=dx)
        electric_power_value = integrate.simpson(electric_power_profile, dx=dx)
        value = cost_value/electric_power_value

        return value
    
class RelativeOperationalCostOfADR(KPI):
    """Ratio between the total operational cost with ADR and the total operational 
    cost in the case of no ADR participation (only fuel cost)."""

    NAME = 'relative operational cost of ADR'
    DEFINITION = __doc__
    UNIT = Unit(numerator=[BaseUnit.PERCENT])
    CATEGORY = KPICategory.EF_DEMAND_RESPONSE_COSTS_OR_SAVINGS
    RELEVANCE = Relevance.HIGH
    STAKEHOLDERS = [Stakeholder.BUILDING_OPERATOR, Stakeholder.BUILDING_OWNER]
    COMPLEXITY = Complexity.LOW
    NEED_BASELINE = True
    TEMPORAL_EVALUATION_WINDOW = TemporalEvaluationWindow.WHOLE_YEAR
    TEMPORAL_RESOLUTION = TemporalResolution.UNSPECIFIED
    SPATIAL_RESOLUTION = SpatialResolution.BUILDING_CLUSTER
    DOE_FLEXIBILITY_CATEGORY = [DOEFlexibilityCategory.LOAD_SHEDDING, DOEFlexibilityCategory.LOAD_SHIFTING, DOEFlexibilityCategory.GENERATION]
    PERFORMANCE_ASPECT = [PerformanceAspect.COST]

    def __init__(self):
        super().__init__()

    @classmethod
    def calculate(
        cls,
        baseline_cost_profile: List[float],
        flexible_cost_profile: List[float],
        timestamps: Union[List[int], List[datetime.datetime], List[str]] = None,
        evaluation_start_timestamp: Union[int, datetime.datetime, str] = None,
        evaluation_end_timestamp: Union[int, datetime.datetime, str] = None,
    ) -> List[float]:
        _, vs = super().calculate(
            baseline_cost_profile=baseline_cost_profile,
            flexible_cost_profile=flexible_cost_profile,
            timestamps=timestamps,
            evaluation_start_timestamp=evaluation_start_timestamp,
            evaluation_end_timestamp=evaluation_end_timestamp,
        )
        
        value = vs.flexible_cost_profile.value[vs.evaluation_mask]/vs.baseline_cost_profile.value[vs.evaluation_mask]

        return value
    
class CostSavings(KPI):
    """Economic savings generated by the demand response of the building when 
    sold on the flexibility market."""

    NAME = 'cost savings'
    DEFINITION = __doc__
    UNIT = Unit(numerator=[BaseUnit.DOLLAR])
    CATEGORY = KPICategory.EF_DEMAND_RESPONSE_COSTS_OR_SAVINGS
    RELEVANCE = Relevance.MEDIUM
    STAKEHOLDERS = [Stakeholder.BUILDING_OPERATOR, Stakeholder.BUILDING_OWNER]
    COMPLEXITY = Complexity.LOW
    NEED_BASELINE = True
    TEMPORAL_EVALUATION_WINDOW = TemporalEvaluationWindow.WHOLE_DAY
    TEMPORAL_RESOLUTION = TemporalResolution.HOURLY
    SPATIAL_RESOLUTION = SpatialResolution.UNSPECIFIED
    DOE_FLEXIBILITY_CATEGORY = [DOEFlexibilityCategory.LOAD_SHEDDING, DOEFlexibilityCategory.LOAD_SHIFTING]
    PERFORMANCE_ASPECT = [PerformanceAspect.COST]

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