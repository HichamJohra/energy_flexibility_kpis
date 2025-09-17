import datetime
from typing import List, Union
import numpy as np
from scipy import integrate
from energy_flexibility_kpis.kpi.base import KPI
from energy_flexibility_kpis.enumerations import BaseUnit, Complexity, DOEFlexibilityCategory, KPICategory, PerformanceAspect, Relevance 
from energy_flexibility_kpis.enumerations import Stakeholder, TemporalEvaluationWindow,TemporalResolution, SpatialResolution
from energy_flexibility_kpis.unit import Unit

class SelfConsumptionDuringDRAction(KPI):
    """The proportion of increased demand covered by onsite generation. This indicator 
    is a measure of the coincidence between locally produced electricity and increased 
    demand during a DR action."""

    NAME = 'self-consumption during DR action'
    DEFINITION = __doc__
    UNIT = Unit(numerator=[BaseUnit.PERCENT])
    CATEGORY = KPICategory.EF_GRID_INTERACTION
    RELEVANCE = Relevance.HIGH
    STAKEHOLDERS = [Stakeholder.BUILDING_OWNER, Stakeholder.BUILDING_OPERATOR]
    COMPLEXITY = Complexity.LOW
    NEED_BASELINE = True
    TEMPORAL_EVALUATION_WINDOW = TemporalEvaluationWindow.UNSPECIFIED
    TEMPORAL_RESOLUTION = TemporalResolution.UNSPECIFIED
    SPATIAL_RESOLUTION = SpatialResolution.SINGLE_BUILDING
    DOE_FLEXIBILITY_CATEGORY = [DOEFlexibilityCategory.LOAD_SHIFTING, DOEFlexibilityCategory.GENERATION]
    PERFORMANCE_ASPECT = [PerformanceAspect.POWER]

    def __init__(self):
        super().__init__()

    @classmethod
    def calculate(
        cls,
        baseline_electric_power_profile: List[float],
        flexible_electric_power_profile: List[float],
        generic_self_production_profile: List[float],
        timestamps: Union[List[int], List[datetime.datetime], List[str]],
        evaluation_start_timestamp: Union[int, datetime.datetime, str] = None,
        evaluation_end_timestamp: Union[int, datetime.datetime, str] = None,
    ) -> float:
        _, vs = super().calculate(
            baseline_electric_power_profile=baseline_electric_power_profile,
            flexible_electric_power_profile=flexible_electric_power_profile,
            generic_self_production_profile=generic_self_production_profile,
            timestamps=timestamps,
            evaluation_start_timestamp=evaluation_start_timestamp,
            evaluation_end_timestamp=evaluation_end_timestamp,
        )
        
        numerator_profile = np.clip(np.min([
            vs.flexible_electric_power_profile.value[vs.evaluation_mask], 
            vs.generic_self_production_profile.value[vs.evaluation_mask]
        ], axis=0) - vs.baseline_electric_power_profile.value[vs.evaluation_mask], min=0.0) 
        denominator_profile = vs.flexible_electric_power_profile.value[vs.evaluation_mask] - vs.baseline_electric_power_profile.value[vs.evaluation_mask]
        dx = vs.get_temporal_resolution(BaseUnit.HOUR, value=vs.timestamps.value[vs.evaluation_mask])
        value = integrate.simpson(numerator_profile, dx=dx)/integrate(denominator_profile, dx=dx)

        return value

class RelativeEnergyImportSavings(KPI):
    """Energy import savings (reduction of the residual power demand that is not covered 
    by local RES production) during demand response period in comparison to the reference 
    operation."""

    NAME = 'relative energy import savings'
    DEFINITION = __doc__
    UNIT = Unit(numerator=[BaseUnit.PERCENT])
    CATEGORY = KPICategory.EF_GRID_INTERACTION
    RELEVANCE = Relevance.LOW
    STAKEHOLDERS = [Stakeholder.BUILDING_OWNER, Stakeholder.BUILDING_OPERATOR]
    COMPLEXITY = Complexity.LOW
    NEED_BASELINE = True
    TEMPORAL_EVALUATION_WINDOW = TemporalEvaluationWindow.UNSPECIFIED
    TEMPORAL_RESOLUTION = TemporalResolution.UNSPECIFIED
    SPATIAL_RESOLUTION = SpatialResolution.UNSPECIFIED
    DOE_FLEXIBILITY_CATEGORY = [DOEFlexibilityCategory.LOAD_SHIFTING, DOEFlexibilityCategory.LOAD_SHEDDING]
    PERFORMANCE_ASPECT = [PerformanceAspect.ENERGY]

    def __init__(self):
        super().__init__()

    @classmethod
    def calculate(
        cls,
        baseline_electric_power_profile: List[float],
        flexible_electric_power_profile: List[float],
        generic_self_production_profile: List[float],
        timestamps: Union[List[int], List[datetime.datetime], List[str]],
        evaluation_start_timestamp: Union[int, datetime.datetime, str] = None,
        evaluation_end_timestamp: Union[int, datetime.datetime, str] = None,
    ) -> float:
        _, vs = super().calculate(
            baseline_electric_power_profile=baseline_electric_power_profile,
            flexible_electric_power_profile=flexible_electric_power_profile,
            generic_self_production_profile=generic_self_production_profile,
            timestamps=timestamps,
            evaluation_start_timestamp=evaluation_start_timestamp,
            evaluation_end_timestamp=evaluation_end_timestamp,
        )
        
        baseline_residual_profile = np.clip(
            vs.baseline_electric_power_profile.value[vs.evaluation_mask] 
                - vs.generic_self_production_profile.value[vs.evaluation_mask], 
            min=0.0
        )
        flexible_residual_profile = np.clip(
            vs.flexible_electric_power_profile.value[vs.evaluation_mask] 
                - vs.generic_self_production_profile.value[vs.evaluation_mask], 
            min=0.0
        )
        dx = vs.get_temporal_resolution(BaseUnit.HOUR, value=vs.timestamps.value[vs.evaluation_mask])
        numerator_value = integrate.simpson(baseline_residual_profile - flexible_residual_profile, dx=dx)
        denominator_value = integrate.simpson(vs.baseline_electric_power_profile.value[vs.evaluation_mask], dx=dx)
        value = numerator_value/denominator_value

        return value
    
class FlexibilityAggregationSynergyFactor(KPI):
    """Quantify the benefit of aggregating multiple flexible systems by measuring the 
    amount of additional Secondary Frequency Regulation (SFR) capacity that is available 
    from the aggregation relative to the sum of SFR capacities the systems could 
    provide individually."""

    NAME = 'flexibility aggregation synergy factor'
    DEFINITION = __doc__
    UNIT = Unit(numerator=[BaseUnit.DIMENSIONLESS])
    CATEGORY = KPICategory.EF_GRID_INTERACTION
    RELEVANCE = Relevance.HIGH
    STAKEHOLDERS = [Stakeholder.GRID_OPERATOR, Stakeholder.DISTRIBUTION_SYSTEM_OPERATOR, Stakeholder.TRANSMISSION_SYSTEM_OPERATOR]
    COMPLEXITY = Complexity.HIGH
    NEED_BASELINE = False
    TEMPORAL_EVALUATION_WINDOW = TemporalEvaluationWindow.UNSPECIFIED
    TEMPORAL_RESOLUTION = TemporalResolution.UNSPECIFIED
    SPATIAL_RESOLUTION = SpatialResolution.UNSPECIFIED
    DOE_FLEXIBILITY_CATEGORY = None
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