import datetime
from typing import List, Union
from scipy import integrate
from energy_flexibility_kpis.kpi.base import KPI
from energy_flexibility_kpis.enumerations import BaseUnit, Complexity, DOEFlexibilityCategory, KPICategory, PerformanceAspect, Relevance 
from energy_flexibility_kpis.enumerations import Stakeholder, TemporalEvaluationWindow,TemporalResolution, SpatialResolution
from energy_flexibility_kpis.unit import Unit

class EnergySavingsOfDemandResponse(KPI):
    """Difference between reference energy usage without demand response and and the energy 
    usage with demand response over the next 24h."""

    NAME = 'energy savings of demand response'
    DEFINITION = __doc__
    UNIT = Unit(numerator=[BaseUnit.KW, BaseUnit.HOUR])
    CATEGORY = KPICategory.EF_DEMAND_RESPONSE_ENERGY_EFFICIENCY
    RELEVANCE = Relevance.MEDIUM
    STAKEHOLDERS = [Stakeholder.BUILDING_OWNER, Stakeholder.BUILDING_OPERATOR]
    COMPLEXITY = Complexity.LOW
    NEED_BASELINE = True
    TEMPORAL_EVALUATION_WINDOW = TemporalEvaluationWindow.WHOLE_DAY
    TEMPORAL_RESOLUTION = TemporalResolution.HOURLY
    SPATIAL_RESOLUTION = SpatialResolution.UNSPECIFIED
    DOE_FLEXIBILITY_CATEGORY = [DOEFlexibilityCategory.EFFICIENCY]
    PERFORMANCE_ASPECT = [PerformanceAspect.ENERGY]

    def __init__(self):
        super().__init__()

    @classmethod
    def calculate(
        cls,
        baseline_electric_power_profile: List[float],
        flexible_electric_power_profile: List[float],
        timestamps: Union[List[int], List[datetime.datetime], List[str]],
        evaluation_start_timestamp: Union[int, datetime.datetime, str] = None,
        evaluation_end_timestamp: Union[int, datetime.datetime, str] = None,
    ) -> float:
        _, vs = super().calculate(
            baseline_electric_power_profile=baseline_electric_power_profile,
            flexible_electric_power_profile=flexible_electric_power_profile,
            timestamps=timestamps,
            evaluation_start_timestamp=evaluation_start_timestamp,
            evaluation_end_timestamp=evaluation_end_timestamp,
        )
        
        profile = vs.flexible_electric_power_profile.value[vs.evaluation_mask] - vs.baseline_electric_power_profile.value[vs.evaluation_mask]
        dx = vs.get_temporal_resolution(BaseUnit.HOUR, value=vs.timestamps.value[vs.evaluation_mask])
        value = integrate.simpson(profile, dx=dx)

        return value

class EnergyConsumptionRatio(KPI):
    """Change in the total energy consumption when implementing an energy flexibility control strategy."""

    NAME = 'energy consumption ratio'
    DEFINITION = __doc__
    UNIT = Unit(numerator=[BaseUnit.DIMENSIONLESS])
    CATEGORY = KPICategory.EF_DEMAND_RESPONSE_ENERGY_EFFICIENCY
    RELEVANCE = Relevance.MEDIUM
    STAKEHOLDERS = [Stakeholder.BUILDING_OPERATOR]
    COMPLEXITY = Complexity.LOW
    NEED_BASELINE = True
    TEMPORAL_EVALUATION_WINDOW = TemporalEvaluationWindow.SINGLE_EVENT
    TEMPORAL_RESOLUTION = TemporalResolution.HOURLY
    SPATIAL_RESOLUTION = SpatialResolution.UNSPECIFIED
    DOE_FLEXIBILITY_CATEGORY = [DOEFlexibilityCategory.EFFICIENCY, DOEFlexibilityCategory.LOAD_SHEDDING]
    PERFORMANCE_ASPECT = [PerformanceAspect.ENERGY]

    def __init__(self):
        super().__init__()

    @classmethod
    def calculate(
        cls,
        baseline_electric_power_profile: List[float],
        flexible_electric_power_profile: List[float],
        timestamps: Union[List[int], List[datetime.datetime], List[str]],
        evaluation_start_timestamp: Union[int, datetime.datetime, str] = None,
        evaluation_end_timestamp: Union[int, datetime.datetime, str] = None,
    ) -> float:
        _, vs = super().calculate(
            baseline_electric_power_profile=baseline_electric_power_profile,
            flexible_electric_power_profile=flexible_electric_power_profile,
            timestamps=timestamps,
            evaluation_start_timestamp=evaluation_start_timestamp,
            evaluation_end_timestamp=evaluation_end_timestamp,
        )
        
        baseline_profile = vs.baseline_electric_power_profile.value[vs.evaluation_mask]
        flexible_profile = vs.flexible_electric_power_profile.value[vs.evaluation_mask]
        dx = vs.get_temporal_resolution(BaseUnit.HOUR, value=vs.timestamps.value[vs.evaluation_mask])
        value = integrate.simpson(flexible_profile, dx=dx)/integrate.simpson(baseline_profile, dx=dx)

        return value
    
class DemandRecoveryRatio(KPI):
    """Ratio between the observed electric energy use by the flexible electric heating systems 
    and the minimum electric energy use of those heating systems, quantifying the increase in 
    energy use due to load shifting. When the heating systems do not interact with the 
    electricity generation system, an optimisation towards minimum electrical energy use is 
    performed at the demand side. The DRR will therefore always be greater than or equal to 1."""

    NAME = 'demand recovery ratio'
    DEFINITION = __doc__
    UNIT = Unit(numerator=[BaseUnit.DIMENSIONLESS])
    CATEGORY = KPICategory.EF_DEMAND_RESPONSE_ENERGY_EFFICIENCY
    RELEVANCE = Relevance.MEDIUM
    STAKEHOLDERS = [Stakeholder.BUILDING_OPERATOR]
    COMPLEXITY = Complexity.LOW
    NEED_BASELINE = True
    TEMPORAL_EVALUATION_WINDOW = TemporalEvaluationWindow.SINGLE_EVENT
    TEMPORAL_RESOLUTION = TemporalResolution.UNSPECIFIED
    SPATIAL_RESOLUTION = SpatialResolution.SINGLE_BUILDING
    DOE_FLEXIBILITY_CATEGORY = [DOEFlexibilityCategory.EFFICIENCY, DOEFlexibilityCategory.LOAD_SHIFTING, DOEFlexibilityCategory.GENERATION]
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
    ) -> List[float]:
        _, vs = super().calculate(
            baseline_electricity_consumption_profile=baseline_electricity_consumption_profile,
            flexible_electricity_consumption_profile=flexible_electricity_consumption_profile,
            timestamps=timestamps,
            evaluation_start_timestamp=evaluation_start_timestamp,
            evaluation_end_timestamp=evaluation_end_timestamp,
        )
        
        flexible_profile = vs.flexible_electricity_consumption_profile.value[vs.evaluation_mask]
        baseline_profile = vs.baseline_electricity_consumption_profile.value[vs.evaluation_mask]
        minimum_energy = min(flexible_profile.min(), baseline_profile.min())
        value = flexible_profile/minimum_energy

        return value
    
class ConsistencyWithEnergySavings(KPI):
    """This index compares the energy reduction in the optimized and most energy efficient scenario, respectively."""

    NAME = 'consistency with energy savings'
    DEFINITION = __doc__
    UNIT = Unit(numerator=[BaseUnit.DIMENSIONLESS])
    CATEGORY = KPICategory.EF_DEMAND_RESPONSE_ENERGY_EFFICIENCY
    RELEVANCE = Relevance.LOW
    STAKEHOLDERS = [Stakeholder.BUILDING_OWNER, Stakeholder.BUILDING_OPERATOR]
    COMPLEXITY = Complexity.LOW
    NEED_BASELINE = True
    TEMPORAL_EVALUATION_WINDOW = TemporalEvaluationWindow.SINGLE_EVENT
    TEMPORAL_RESOLUTION = TemporalResolution.UNSPECIFIED
    SPATIAL_RESOLUTION = SpatialResolution.UNSPECIFIED
    DOE_FLEXIBILITY_CATEGORY = [DOEFlexibilityCategory.EFFICIENCY]
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
        
        raise NotImplementedError('Variables are unclear')