import datetime
from typing import List, Union
import numpy as np
from energy_flexibility_kpis.kpi.base import KPI
from energy_flexibility_kpis.enumerations import BaseUnit, Complexity, DOEFlexibilityCategory, KPICategory, PerformanceAspect, Relevance 
from energy_flexibility_kpis.enumerations import Stakeholder, TemporalEvaluationWindow,TemporalResolution, SpatialResolution
from energy_flexibility_kpis.unit import Unit

class DeviationDecreaseFromTheFlatDemandProfile(KPI):
    """This index evaluate the ability of power flexibility in the modification of 
    a building demand profile focusing on the variance of the demand profile (y values)."""

    NAME = 'deviation decrease from the flat demand profile'
    DEFINITION = __doc__
    UNIT = Unit(numerator=[BaseUnit.DIMENSIONLESS])
    CATEGORY = KPICategory.EF_DEMAND_PROFILE_RESHAPING
    RELEVANCE = Relevance.LOW
    STAKEHOLDERS = [Stakeholder.GRID_OPERATOR, Stakeholder.DISTRIBUTION_SYSTEM_OPERATOR]
    COMPLEXITY = Complexity.LOW
    NEED_BASELINE = True
    TEMPORAL_EVALUATION_WINDOW = TemporalEvaluationWindow.WHOLE_DAY
    TEMPORAL_RESOLUTION = TemporalResolution.UNSPECIFIED
    SPATIAL_RESOLUTION = SpatialResolution.UNSPECIFIED
    DOE_FLEXIBILITY_CATEGORY = [DOEFlexibilityCategory.LOAD_SHEDDING]
    PERFORMANCE_ASPECT = [PerformanceAspect.ENERGY]

    def __init__(self):
        super().__init__()

    @classmethod
    def calculate(
        cls,
        baseline_electricity_consumption_profile: List[float], 
        flexible_electricity_consumption_profile: List[float],
        timestamps: Union[List[int], List[datetime.datetime], List[str]] = None,
        evaluation_start_timestamp: Union[int, datetime.datetime, str] = None,
        evaluation_end_timestamp: Union[int, datetime.datetime, str] = None,
    ) -> float:
        _, vs = super().calculate(
            timestamps=timestamps,
            baseline_electricity_consumption_profile=baseline_electricity_consumption_profile,
            flexible_electricity_consumption_profile=flexible_electricity_consumption_profile,
            evaluation_start_timestamp=evaluation_start_timestamp,
            evaluation_end_timestamp=evaluation_end_timestamp,
        )
        
        value = 1.0 - (
            np.var(vs.flexible_electricity_consumption_profile.value[vs.evaluation_mask])
            /np.var(vs.baseline_electricity_consumption_profile.value[vs.evaluation_mask])
        )**0.5

        return value

class FlexibilityMap(KPI):
    """Flexibility map (upward and downward load profile for the next 24h). Calculated 
    by MPC with black box model of the building and energy price forecast."""

    NAME = 'flexibility map'
    DEFINITION = __doc__
    UNIT = Unit(numerator=[BaseUnit.KW, BaseUnit.HOUR])
    CATEGORY = KPICategory.EF_DEMAND_PROFILE_RESHAPING
    RELEVANCE = Relevance.MEDIUM
    STAKEHOLDERS = [Stakeholder.GRID_OPERATOR, Stakeholder.BUILDING_OPERATOR]
    COMPLEXITY = Complexity.HIGH
    NEED_BASELINE = True
    TEMPORAL_EVALUATION_WINDOW = TemporalEvaluationWindow.WHOLE_DAY
    TEMPORAL_RESOLUTION = TemporalResolution.UNSPECIFIED
    SPATIAL_RESOLUTION = SpatialResolution.UNSPECIFIED
    DOE_FLEXIBILITY_CATEGORY = [DOEFlexibilityCategory.LOAD_SHEDDING]
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
        
        raise NotImplementedError('Has no equation. Requires MPC with black box model.')
    
class Ramp(KPI):
    """Ramp of the power consumption."""

    NAME = 'ramp'
    DEFINITION = __doc__
    UNIT = Unit(numerator=[BaseUnit.KW])
    CATEGORY = KPICategory.EF_DEMAND_PROFILE_RESHAPING
    RELEVANCE = Relevance.LOW
    STAKEHOLDERS = [Stakeholder.GRID_OPERATOR, Stakeholder.DISTRIBUTION_SYSTEM_OPERATOR]
    COMPLEXITY = Complexity.LOW
    NEED_BASELINE = False
    TEMPORAL_EVALUATION_WINDOW = TemporalEvaluationWindow.SINGLE_EVENT
    TEMPORAL_RESOLUTION = TemporalResolution.HOURLY
    SPATIAL_RESOLUTION = SpatialResolution.UNSPECIFIED
    DOE_FLEXIBILITY_CATEGORY = [DOEFlexibilityCategory.MODULATING]
    PERFORMANCE_ASPECT = [PerformanceAspect.ENERGY, PerformanceAspect.POWER]

    def __init__(self):
        super().__init__()

    @classmethod
    def calculate(
        cls,
        generic_electric_power_profile: List[float],
        timestamps: Union[List[int], List[datetime.datetime], List[str]] = None,
        evaluation_start_timestamp: Union[int, datetime.datetime, str] = None,
        evaluation_end_timestamp: Union[int, datetime.datetime, str] = None,
    ) -> List[float]:
        _, vs = super().calculate(
            timestamps=timestamps,
            generic_electric_power_profile=generic_electric_power_profile,
            evaluation_start_timestamp=evaluation_start_timestamp,
            evaluation_end_timestamp=evaluation_end_timestamp,
        )
        
        value = vs.generic_electric_power_profile.value[vs.evaluation_mask] - np.roll(vs.generic_electric_power_profile.value[vs.evaluation_mask], 1)
        if value.dtype != float:
            value = value.astype(float)
        value[0] = np.nan

        return value