import datetime
from typing import List, Union
import pandas as pd
from energy_flexibility_kpis.kpi.base import KPI
from energy_flexibility_kpis.enumerations import BaseUnit, Complexity, DOEFlexibilityCategory, KPICategory, PerformanceAspect, Relevance 
from energy_flexibility_kpis.enumerations import Stakeholder, TemporalEvaluationWindow,TemporalResolution, SpatialResolution
from energy_flexibility_kpis.unit import Unit
from energy_flexibility_kpis.variable import Variable

class PeakPowerReduction(KPI):
    """Reduced power demand during peak hour due to flexible operation."""

    NAME = 'peak power reduction'
    DEFINITION = __doc__
    UNIT = Unit(numerator=[BaseUnit.KW])
    CATEGORY = KPICategory.EF_PEAK_POWER_SHEDDING
    RELEVANCE = Relevance.HIGH
    STAKEHOLDERS = [Stakeholder.DISTRIBUTION_SYSTEM_OPERATOR, Stakeholder.TRANSMISSION_SYSTEM_OPERATOR]
    COMPLEXITY = Complexity.LOW
    NEED_BASELINE = True
    TEMPORAL_EVALUATION_WINDOW = TemporalEvaluationWindow.SINGLE_EVENT
    TEMPORAL_RESOLUTION = TemporalResolution.HOURLY
    SPATIAL_RESOLUTION = SpatialResolution.UNSPECIFIED
    DOE_FLEXIBILITY_CATEGORY = [DOEFlexibilityCategory.LOAD_SHEDDING]
    PERFORMANCE_ASPECT = [PerformanceAspect.POWER]

    def __init__(self):
        super().__init__()

    @classmethod
    def calculate(
        cls,
        baseline_electric_power_profile: List[float], 
        flexible_electric_power_profile: List[float],
        timestamps: Union[List[int], List[datetime.datetime], List[str]] = None,
        evaluation_start_timestamp: Union[int,datetime.datetime, str] = None,
        evaluation_end_timestamp: Union[int,datetime.datetime, str] = None,
    ) -> Union[float, List[float]]:
        _, vs = super().calculate(
            baseline_electric_power_profile=baseline_electric_power_profile,
            flexible_electric_power_profile=flexible_electric_power_profile,
            timestamps=timestamps,
            evaluation_start_timestamp=evaluation_start_timestamp,
            evaluation_end_timestamp=evaluation_end_timestamp,
        )

        value = vs.baseline_electric_power_profile.value[vs.evaluation_mask] - vs.flexible_electric_power_profile.value[vs.evaluation_mask]

        return value
    
class HourlyRelativePowerDemandReduction(KPI):
    """Reduced power demand during peak hour due to flexible operation."""

    NAME = 'hourly relative power demand reduction'
    DEFINITION = __doc__
    UNIT = Unit(numerator=[BaseUnit.KW])
    CATEGORY = KPICategory.EF_PEAK_POWER_SHEDDING
    RELEVANCE = Relevance.HIGH
    STAKEHOLDERS = [Stakeholder.DISTRIBUTION_SYSTEM_OPERATOR, Stakeholder.GRID_OPERATOR]
    COMPLEXITY = Complexity.LOW
    NEED_BASELINE = True
    TEMPORAL_EVALUATION_WINDOW = TemporalEvaluationWindow.SINGLE_EVENT
    TEMPORAL_RESOLUTION = TemporalResolution.HOURLY
    SPATIAL_RESOLUTION = SpatialResolution.UNSPECIFIED
    DOE_FLEXIBILITY_CATEGORY = [DOEFlexibilityCategory.LOAD_SHEDDING]
    PERFORMANCE_ASPECT = [PerformanceAspect.POWER]

    def __init__(self):
        super().__init__()

    @classmethod
    def calculate(
        baseline_electric_power_profile: List[float], 
        flexible_electric_power_profile: List[float],
        timestamps: Union[ List[int], List[datetime.datetime], List[str]] = None,
        evaluation_start_timestamp: Union[int, datetime.datetime, str] = None,
        evaluation_end_timestamp: Union[int, datetime.datetime, str] = None,
    ) -> Union[float, List[float]]:
        _, vs = super().calculate(
            baseline_electric_power_profile=baseline_electric_power_profile,
            flexible_electric_power_profile=flexible_electric_power_profile,
            timestamps=timestamps,
            evaluation_start_timestamp=evaluation_start_timestamp,
            evaluation_end_timestamp=evaluation_end_timestamp,
        )

        value = (vs.baseline_electric_power_profile.value[vs.evaluation_mask]
                    - vs.flexible_electric_power_profile.value[vs.evaluation_mask]
        )/vs.baseline_electric_power_profile.value[vs.evaluation_mask]

        return value
    
class RelativePeakPowerDemandReduction(KPI):
    """Percentage of power demand reduction during peak hour due to flexible operation."""

    NAME = 'relative peak power demand reduction'
    DEFINITION = __doc__
    UNIT = Unit(numerator=[BaseUnit.PERCENT])
    CATEGORY = KPICategory.EF_PEAK_POWER_SHEDDING
    RELEVANCE = Relevance.HIGH
    STAKEHOLDERS = [Stakeholder.DISTRIBUTION_SYSTEM_OPERATOR, Stakeholder.GRID_OPERATOR]
    COMPLEXITY = Complexity.MEDIUM
    NEED_BASELINE = True
    TEMPORAL_EVALUATION_WINDOW = TemporalEvaluationWindow.SINGLE_EVENT
    TEMPORAL_RESOLUTION = TemporalResolution.HOURLY
    SPATIAL_RESOLUTION = SpatialResolution.UNSPECIFIED
    DOE_FLEXIBILITY_CATEGORY = [DOEFlexibilityCategory.LOAD_SHEDDING]
    PERFORMANCE_ASPECT = [PerformanceAspect.POWER]

    def __init__(self):
        super().__init__()

    @classmethod
    def calculate(
        baseline_electric_power_profile: List[float], 
        flexible_electric_power_profile: List[float],
        timestamps: Union[List[int], List[datetime.datetime], List[str]] = None,
        evaluation_start_timestamp: Union[int, datetime.datetime, str] = None,
        evaluation_end_timestamp: Union[int, datetime.datetime, str] = None,
    ) -> Union[float, List[float]]:
        _, vs = super().calculate(
            baseline_electric_power_profile=baseline_electric_power_profile,
            flexible_electric_power_profile=flexible_electric_power_profile,
            timestamps=timestamps,
            evaluation_start_timestamp=evaluation_start_timestamp,
            evaluation_end_timestamp=evaluation_end_timestamp,
        )

        value = 1 - (
            vs.flexible_electric_power_profile.value[vs.evaluation_mask]
                /vs.baseline_electric_power_profile.value[vs.evaluation_mask]
        )

        return value
    
class PowerPaybackRatio(KPI):
    """Quantify variation of peak with / without DR -- For  DSO-TSO."""

    NAME = 'power payback ratio'
    DEFINITION = __doc__
    UNIT = Unit(numerator=[BaseUnit.DIMENSIONLESS])
    CATEGORY = KPICategory.EF_PEAK_POWER_SHEDDING
    RELEVANCE = Relevance.HIGH
    STAKEHOLDERS = [Stakeholder.DISTRIBUTION_SYSTEM_OPERATOR, Stakeholder.TRANSMISSION_SYSTEM_OPERATOR]
    COMPLEXITY = Complexity.LOW
    NEED_BASELINE = True
    TEMPORAL_EVALUATION_WINDOW = TemporalEvaluationWindow.UNSPECIFIED
    TEMPORAL_RESOLUTION = TemporalResolution.UNSPECIFIED
    SPATIAL_RESOLUTION = SpatialResolution.BUILDING_CLUSTER
    DOE_FLEXIBILITY_CATEGORY = [DOEFlexibilityCategory.LOAD_SHIFTING, DOEFlexibilityCategory.LOAD_SHEDDING]
    PERFORMANCE_ASPECT = [PerformanceAspect.POWER]

    def __init__(self):
        super().__init__()

    @classmethod
    def calculate(
        resource_ids: Union[List[int], List[str]],
        availability: Union[List[int], List[bool]],
        baseline_electric_power_profile: Union[Variable, List[float]],
        flexible_electric_power_profile: Union[Variable, List[float]],
        timestamps: Union[Variable, List[int], List[datetime.datetime], List[str]] = None,
        evaluation_start_timestamp: Union[Variable, int,datetime.datetime, str] = None,
        evaluation_end_timestamp: Union[Variable, int,datetime.datetime, str] = None,
    ) -> float:
        _, vs = super().calculate(
            resource_ids=resource_ids,
            availability=availability,
            baseline_electric_power_profile=baseline_electric_power_profile,
            flexible_electric_power_profile=flexible_electric_power_profile,
            timestamps=timestamps,
            evaluation_start_timestamp=evaluation_start_timestamp,
            evaluation_end_timestamp=evaluation_end_timestamp,
        )

        data = pd.DataFrame({
            'resource_id': vs.resource_ids.value[vs.evaluation_mask],
            'baseline_electric_power_profile': vs.baseline_electric_power_profile.value[vs.evaluation_mask]*vs.availability.value[vs.evaluation_mask],
            'flexible_electric_power_profile': vs.flexible_electric_power_profile.value[vs.evaluation_mask]*vs.availability.value[vs.evaluation_mask],
        })
        data['timestep'] = data.groupby('group_id').cumcount()
        data = data.groupby('timestep')[['baseline', 'flexible']].sum()
        value = data['flexible_electric_power_profile'].max()/data['flexible_electric_power_profile'].max()

        return value