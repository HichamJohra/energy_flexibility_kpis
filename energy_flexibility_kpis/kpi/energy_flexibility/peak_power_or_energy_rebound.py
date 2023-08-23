import datetime
from typing import List, Union
from scipy import integrate
from energy_flexibility_kpis.kpi.base import KPI
from energy_flexibility_kpis.enumerations import BaseUnit, Complexity, DOEFlexibilityCategory, KPICategory, PerformanceAspect, Relevance 
from energy_flexibility_kpis.enumerations import Stakeholder, TemporalEvaluationWindow,TemporalResolution, SpatialResolution
from energy_flexibility_kpis.unit import Unit

class PeakPowerRebound(KPI):
    """Power demand increase during peak hour after flexible operation (rebound effect). The evaluation window should be set to the rebound period."""

    NAME = 'peak power rebound'
    DEFINITION = __doc__
    UNIT = Unit(numerator=[BaseUnit.KW])
    CATEGORY = KPICategory.EF_PEAK_POWER_OR_ENERGY_REBOUND
    RELEVANCE = Relevance.HIGH
    STAKEHOLDERS = [Stakeholder.DISTRIBUTION_SYSTEM_OPERATOR, Stakeholder.TRANSMISSION_SYSTEM_OPERATOR]
    COMPLEXITY = Complexity.LOW
    NEED_BASELINE = True
    TEMPORAL_EVALUATION_WINDOW = TemporalEvaluationWindow.SINGLE_EVENT
    TEMPORAL_RESOLUTION = TemporalResolution.UNSPECIFIED
    SPATIAL_RESOLUTION = SpatialResolution.SINGLE_BUILDING
    DOE_FLEXIBILITY_CATEGORY = [DOEFlexibilityCategory.LOAD_SHIFTING, DOEFlexibilityCategory.LOAD_SHEDDING]
    PERFORMANCE_ASPECT = [PerformanceAspect.POWER]

    def __init__(self):
        super().__init__()

    @classmethod
    def calculate(
        cls,
        baseline_electric_power_profile: List[float], 
        flexible_electric_power_profile: List[float],
        timestamps: Union[List[int], List[datetime.datetime], List[str]] = None,
        evaluation_start_timestamp: Union[int, datetime.datetime, str] = None,
        evaluation_end_timestamp: Union[int, datetime.datetime, str] = None,
    ) -> Union[float, List[float]]:
        _, vs = super().calculate(
            timestamps=timestamps,
            baseline_electric_power_profile=baseline_electric_power_profile, 
            flexible_electric_power_profile=flexible_electric_power_profile,
            evaluation_start_timestamp=evaluation_start_timestamp,
            evaluation_end_timestamp=evaluation_end_timestamp,
        )
        
        value = vs.baseline_electric_power_profile.value[vs.evaluation_mask] - vs.flexible_electric_power_profile.value[vs.evaluation_mask]

        return value
    
class AveragePowerRebound(KPI):
    """Average power rebound after DR event compared to baseline. The evaluation window should be set to the rebound period."""

    NAME = 'average power rebound'
    DEFINITION = __doc__
    UNIT = Unit(numerator=[BaseUnit.KW])
    CATEGORY = KPICategory.EF_PEAK_POWER_OR_ENERGY_REBOUND
    RELEVANCE = Relevance.HIGH
    STAKEHOLDERS = [Stakeholder.DISTRIBUTION_SYSTEM_OPERATOR, Stakeholder.TRANSMISSION_SYSTEM_OPERATOR]
    COMPLEXITY = Complexity.LOW
    NEED_BASELINE = True
    TEMPORAL_EVALUATION_WINDOW = TemporalEvaluationWindow.SINGLE_EVENT
    TEMPORAL_RESOLUTION = TemporalResolution.UNSPECIFIED
    SPATIAL_RESOLUTION = SpatialResolution.SINGLE_BUILDING
    DOE_FLEXIBILITY_CATEGORY = [DOEFlexibilityCategory.LOAD_SHIFTING, DOEFlexibilityCategory.LOAD_SHEDDING]
    PERFORMANCE_ASPECT = [PerformanceAspect.POWER]

    def __init__(self):
        super().__init__()

    @classmethod
    def calculate(
        cls,
        baseline_electric_power_profile: List[float], 
        flexible_electric_power_profile: List[float],
        timestamps: Union[List[int], List[datetime.datetime], List[str]] = None,
        evaluation_start_timestamp: Union[int, datetime.datetime, str] = None,
        evaluation_end_timestamp: Union[int, datetime.datetime, str] = None,
    ) -> float:
        _, vs = super().calculate(
            timestamps=timestamps,
            baseline_electric_power_profile=baseline_electric_power_profile,
            flexible_electric_power_profile=flexible_electric_power_profile,
            evaluation_start_timestamp=evaluation_start_timestamp,
            evaluation_end_timestamp=evaluation_end_timestamp,
        )
        
        value = (
            vs.baseline_electric_power_profile.value[vs.evaluation_mask] 
                - vs.flexible_electric_power_profile.value[vs.evaluation_mask]
        ).mean()

        return value
    
class ReboundEnergy(KPI):
    """Size of consumption deviation prior / following an DR event. Important to grid 
    operation to ensure stability / balance outside DR period. The evaluation window should be set to the rebound period."""

    NAME = 'rebound energy'
    DEFINITION = __doc__
    UNIT = Unit(numerator=[BaseUnit.KWH])
    CATEGORY = KPICategory.EF_PEAK_POWER_OR_ENERGY_REBOUND
    RELEVANCE = Relevance.HIGH
    STAKEHOLDERS = [Stakeholder.BUILDING_OWNER, Stakeholder.AGGREGATOR, Stakeholder.GRID_OPERATOR]
    COMPLEXITY = Complexity.LOW
    NEED_BASELINE = True
    TEMPORAL_EVALUATION_WINDOW = TemporalEvaluationWindow.SINGLE_EVENT
    TEMPORAL_RESOLUTION = TemporalResolution.UNSPECIFIED
    SPATIAL_RESOLUTION = SpatialResolution.SINGLE_BUILDING
    DOE_FLEXIBILITY_CATEGORY = [DOEFlexibilityCategory.LOAD_SHIFTING, DOEFlexibilityCategory.LOAD_SHEDDING]
    PERFORMANCE_ASPECT = [PerformanceAspect.ENERGY]

    def __init__(self):
        super().__init__()

    @classmethod
    def calculate(
        cls,
        baseline_electric_power_profile: List[float], 
        flexible_electric_power_profile: List[float],
        high_price_start_timestamp: Union[str, datetime.datetime, int],
        high_price_end_timestamp: Union[str, datetime.datetime, int],
        timestamps: Union[List[int], List[datetime.datetime], List[str]],
        evaluation_start_timestamp: Union[int, datetime.datetime, str] = None,
        evaluation_end_timestamp: Union[int, datetime.datetime, str] = None,
    ) -> float:
        """Assumes timestamps is in hours when calculating integral."""
        
        _, vs = super().calculate(
            timestamps=timestamps,
            baseline_electric_power_profile=baseline_electric_power_profile,
            flexible_electric_power_profile=flexible_electric_power_profile,
            high_price_start_timestamp=high_price_start_timestamp,
            high_price_end_timestamp=high_price_end_timestamp,
            evaluation_start_timestamp=evaluation_start_timestamp,
            evaluation_end_timestamp=evaluation_end_timestamp,
        )
        
        pre_event_timestamp_mask = vs.evaluation_mask & (vs.timestamps.value < vs.high_price_start_timestamp.value)
        post_event_timestamp_mask = vs.evaluation_mask & (vs.timestamps.value > vs.high_price_start_timestamp.value)

        pre_event_flexible_electric_power_profile = vs.flexible_electric_power_profile.value[pre_event_timestamp_mask]
        post_event_flexible_electric_power_profile = vs.flexible_electric_power_profile.value[post_event_timestamp_mask]
        pre_event_baseline_electric_power_profile = vs.baseline_electric_power_profile.value[pre_event_timestamp_mask]
        post_event_baseline_electric_power_profile = vs.baseline_electric_power_profile.value[post_event_timestamp_mask]

        pre_event_profile = pre_event_flexible_electric_power_profile - pre_event_baseline_electric_power_profile
        post_event_profile = post_event_flexible_electric_power_profile - post_event_baseline_electric_power_profile
        pre_event_timestamps = vs.timestamps.value[pre_event_timestamp_mask]
        post_event_timestamps = vs.timestamps.value[post_event_timestamp_mask]
        pre_event_value = integrate.simps(pre_event_profile, pre_event_timestamps)
        post_event_value = integrate.simps(post_event_profile, post_event_timestamps)
        value = pre_event_value + post_event_value

        return value