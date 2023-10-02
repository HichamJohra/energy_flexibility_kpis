import datetime
from typing import List, Union
from scipy import integrate
from energy_flexibility_kpis.kpi.base import KPI
from energy_flexibility_kpis.enumerations import BaseUnit, Complexity, DOEFlexibilityCategory, KPICategory, PerformanceAspect, Relevance 
from energy_flexibility_kpis.enumerations import Stakeholder, TemporalEvaluationWindow,TemporalResolution, SpatialResolution
from energy_flexibility_kpis.unit import Unit

class RelativeCO2EmissionsReduction(KPI):
    """CO2 emissions savings due to the demand response of the building."""

    NAME = 'relative CO2 emissions reduction'
    DEFINITION = __doc__
    UNIT = Unit(numerator=[BaseUnit.PERCENT])
    CATEGORY = KPICategory.EF_DEMAND_RESPONSE_EMISSION_OR_ENVIRONMENTAL_IMPACT
    RELEVANCE = Relevance.MEDIUM
    STAKEHOLDERS = [Stakeholder.GRID_OPERATOR, Stakeholder.POLICYMAKER, Stakeholder.UTILITY_COMPANY]
    COMPLEXITY = Complexity.LOW
    NEED_BASELINE = True
    TEMPORAL_EVALUATION_WINDOW = TemporalEvaluationWindow.UNSPECIFIED
    TEMPORAL_RESOLUTION = TemporalResolution.UNSPECIFIED
    SPATIAL_RESOLUTION = SpatialResolution.UNSPECIFIED
    DOE_FLEXIBILITY_CATEGORY = [DOEFlexibilityCategory.LOAD_SHEDDING, DOEFlexibilityCategory.LOAD_SHIFTING]
    PERFORMANCE_ASPECT = [PerformanceAspect.EMISSION]

    def __init__(self):
        super().__init__()

    @classmethod
    def calculate(
        cls,
        baseline_carbon_emissions_profile: List[float],
        flexible_carbon_emissions_profile: List[float],
        timestamps: Union[List[int], List[datetime.datetime], List[str]] = None,
        evaluation_start_timestamp: Union[int, datetime.datetime, str] = None,
        evaluation_end_timestamp: Union[int, datetime.datetime, str] = None,
    ) -> List[float]:
        _, vs = super().calculate(
            baseline_carbon_emissions_profile=baseline_carbon_emissions_profile,
            flexible_carbon_emissions_profile=flexible_carbon_emissions_profile,
            timestamps=timestamps,
            evaluation_start_timestamp=evaluation_start_timestamp,
            evaluation_end_timestamp=evaluation_end_timestamp,
        )
        
        value = (
            vs.flexible_carbon_emissions_profile.value[vs.evaluation_mask] 
                - vs.baseline_carbon_emissions_profile.value[vs.evaluation_mask]
        )*100.0/vs.baseline_carbon_emissions_profile.value[vs.evaluation_mask]

        return value
    
class EnvironmentalSavings(KPI):
    """CO2 emissions savings due to the demand response of the building."""

    NAME = 'environmental savings'
    DEFINITION = __doc__
    UNIT = Unit(numerator=[BaseUnit.KG_OF_CO2])
    CATEGORY = KPICategory.EF_DEMAND_RESPONSE_EMISSION_OR_ENVIRONMENTAL_IMPACT
    RELEVANCE = Relevance.MEDIUM
    STAKEHOLDERS = [Stakeholder.GRID_OPERATOR, Stakeholder.POLICYMAKER, Stakeholder.UTILITY_COMPANY]
    COMPLEXITY = Complexity.LOW
    NEED_BASELINE = True
    TEMPORAL_EVALUATION_WINDOW = TemporalEvaluationWindow.WHOLE_DAY
    TEMPORAL_RESOLUTION = TemporalResolution.HOURLY
    SPATIAL_RESOLUTION = SpatialResolution.UNSPECIFIED
    DOE_FLEXIBILITY_CATEGORY = [DOEFlexibilityCategory.LOAD_SHEDDING, DOEFlexibilityCategory.LOAD_SHIFTING]
    PERFORMANCE_ASPECT = [PerformanceAspect.EMISSION]

    def __init__(self):
        super().__init__()

    @classmethod
    def calculate(
        cls,
        baseline_electric_power_profile: List[float],
        flexible_electric_power_profile: List[float],
        generic_carbon_intensity_profile: List[float],
        timestamps: Union[List[int], List[datetime.datetime], List[str]],
        evaluation_start_timestamp: Union[int, datetime.datetime, str] = None,
        evaluation_end_timestamp: Union[int, datetime.datetime, str] = None,
    ) -> float:
        _, vs = super().calculate(
            baseline_electric_power_profile=baseline_electric_power_profile,
            flexible_electric_power_profile=flexible_electric_power_profile,
            generic_carbon_intensity_profile=generic_carbon_intensity_profile,
            timestamps=timestamps,
            evaluation_start_timestamp=evaluation_start_timestamp,
            evaluation_end_timestamp=evaluation_end_timestamp,
        )
        
        electric_power_profile = vs.flexible_electric_power_profile.value[vs.evaluation_mask] - vs.baseline_electric_power_profile.value[vs.evaluation_mask]
        carbon_emissions_profile = electric_power_profile*vs.generic_carbon_intensity_profile.value[vs.evaluation_mask]
        dx = vs.get_temporal_resolution(BaseUnit.HOUR, value=vs.timestamps.value[vs.evaluation_mask])
        value = integrate.simpson(carbon_emissions_profile, dx=dx)

        return value