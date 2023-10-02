import datetime
import inspect
from typing import Any, List, Mapping, Tuple, Union
import numpy as np
from energy_flexibility_kpis.base import Definition 
from energy_flexibility_kpis.enumerations import Complexity, DOEFlexibilityCategory, KPICategory, PerformanceAspect, Relevance 
from energy_flexibility_kpis.enumerations import Stakeholder, TemporalEvaluationWindow,TemporalResolution, SpatialResolution
from energy_flexibility_kpis.unit import Unit
from energy_flexibility_kpis.variable import DefaultVariable, VariableSet

class KPI(Definition):
    NAME: str = 'kpi'
    DEFINITION: str = __doc__
    UNIT: Unit = None
    CATEGORY: KPICategory  = None
    RELEVANCE: Relevance = None
    STAKEHOLDERS: List[Stakeholder] = None
    COMPLEXITY: Complexity = None
    NEED_BASELINE: bool = None
    TEMPORAL_EVALUATION_WINDOW: TemporalEvaluationWindow = TemporalEvaluationWindow.UNSPECIFIED
    TEMPORAL_RESOLUTION: TemporalResolution = TemporalResolution.UNSPECIFIED
    SPATIAL_RESOLUTION: SpatialResolution = SpatialResolution.UNSPECIFIED
    DOE_FLEXIBILITY_CATEGORY: List[DOEFlexibilityCategory] = None
    PERFORMANCE_ASPECT: List[PerformanceAspect] = None

    def __init__(self) -> None:
        pass

    @classmethod
    def info(cls) -> Mapping[str, Any]:
        return {
            'name': cls.NAME,
            'definition': cls.DEFINITION,
            'unit': None if cls.UNIT is None else str(cls.UNIT),
            'category': None if cls.CATEGORY is None else cls.CATEGORY.value[0].value + ': ' + cls.CATEGORY.value[1],
            'relevance': None if cls.RELEVANCE is None else cls.RELEVANCE.value,
            'stakeholders': None if cls.STAKEHOLDERS is None else [s.value for s in cls.STAKEHOLDERS],
            'complexity': None if cls.COMPLEXITY is None else cls.COMPLEXITY.value,
            'need_baseline': cls.NEED_BASELINE,
            'temporal_evaluation_window': cls.TEMPORAL_EVALUATION_WINDOW.value,
            'temporal_resolution': cls.TEMPORAL_RESOLUTION.value,
            'spatial_resolution': cls.SPATIAL_RESOLUTION.value,
            'doe_flexibility_category': None if cls.DOE_FLEXIBILITY_CATEGORY is None else [c.value for c in cls.DOE_FLEXIBILITY_CATEGORY],
            'performance_aspect': None if cls.PERFORMANCE_ASPECT is None else [p.value for p in cls.PERFORMANCE_ASPECT],
            'calculation_arguments': cls.__get_calculate_arguments_info()
        }
    
    @classmethod
    def __get_calculate_arguments_info(cls):
        args = inspect.getfullargspec(cls.calculate).args
        info = []

        for arg in args:
            try:
                info.append(getattr(DefaultVariable, arg).info())

            except AttributeError:
                pass

        return info
    
    @classmethod
    def calculate(
        cls,
        availability: Union[List[int], List[bool]] = None,
        timestamps: Union[List[int], List[datetime.datetime], List[str]] = None,
        evaluation_start_timestamp: Union[int, datetime.datetime, str] = None,
        evaluation_end_timestamp: Union[int, datetime.datetime, str] = None,
        baseline_electric_power_profile: List[float] = None,
        baseline_electricity_consumption_profile: List[float] = None,
        baseline_natural_gas_consumption_profile: List[float] = None,
        baseline_cost_profile: List[float] = None,
        baseline_carbon_emissions_profile: List[float] = None,
        baseline_carbon_intensity_profile: List[float] = None,
        baseline_self_production_profile: List[float] = None,
        flexible_electric_power_profile: List[float] = None,
        flexible_electricity_consumption_profile: List[float] = None,
        flexible_natural_gas_consumption_profile: List[float] = None,
        flexible_cost_profile: List[float] = None,
        flexible_carbon_emissions_profile: List[float] = None,
        flexible_carbon_intensity_profile: List[float] = None,
        flexible_self_production_profile: List[float] = None,
        generic_electric_power_profile: List[float] = None,
        generic_electricity_consumption_profile: List[float] = None,
        generic_natural_gas_consumption_profile: List[float] = None,
        generic_cost_profile: List[float] = None,
        generic_carbon_emissions_profile: List[float] = None,
        generic_carbon_intensity_profile: List[float] = None,
        generic_self_production_profile: List[float] = None,
        load_profile_peak_timestamp: Union[int, datetime.datetime, str] = None,
        load_profile_valley_timestamp: Union[int, datetime.datetime, str] = None,
        grid_peak_timestamp: Union[int, datetime.datetime, str] = None,
        generic_signal_start_timestamp: Union[int, datetime.datetime, str] = None,
        generic_signal_end_timestamp: Union[int, datetime.datetime, str] = None,
        low_generic_signal_start_timestamp: Union[int, datetime.datetime, str] = None,
        low_generic_signal_end_timestamp: Union[int, datetime.datetime, str] = None,
        medium_generic_signal_start_timestamp: Union[int, datetime.datetime, str] = None,
        medium_generic_signal_end_timestamp: Union[int, datetime.datetime, str] = None,
        high_generic_signal_start_timestamp: Union[int, datetime.datetime, str] = None,
        high_generic_signal_end_timestamp: Union[int, datetime.datetime, str] = None,
        high_price_start_timestamp: Union[int, datetime.datetime, str] = None,
        high_price_end_timestamp: Union[int, datetime.datetime, str] = None,
        high_emission_start_timestamp: Union[int, datetime.datetime, str] = None,
        high_emission_end_timestamp: Union[int, datetime.datetime, str] = None,
    ) -> Tuple[Union[float, List[float]], VariableSet]:
        vs = VariableSet(
            availability=availability,
            timestamps=timestamps,
            evaluation_start_timestamp=evaluation_start_timestamp,
            evaluation_end_timestamp=evaluation_end_timestamp,
            baseline_electric_power_profile=baseline_electric_power_profile,
            baseline_electricity_consumption_profile=baseline_electricity_consumption_profile,
            baseline_natural_gas_consumption_profile=baseline_natural_gas_consumption_profile,
            baseline_cost_profile=baseline_cost_profile,
            baseline_carbon_emissions_profile=baseline_carbon_emissions_profile,
            baseline_carbon_intensity_profile=baseline_carbon_intensity_profile,
            baseline_self_production_profile=baseline_self_production_profile,
            flexible_electric_power_profile=flexible_electric_power_profile,
            flexible_electricity_consumption_profile=flexible_electricity_consumption_profile,
            flexible_natural_gas_consumption_profile=flexible_natural_gas_consumption_profile,
            flexible_cost_profile=flexible_cost_profile,
            flexible_carbon_emissions_profile=flexible_carbon_emissions_profile,
            flexible_carbon_intensity_profile=flexible_carbon_intensity_profile,
            flexible_self_production_profile=flexible_self_production_profile,
            generic_electric_power_profile=generic_electric_power_profile,
            generic_electricity_consumption_profile=generic_electricity_consumption_profile,
            generic_natural_gas_consumption_profile=generic_natural_gas_consumption_profile,
            generic_cost_profile=generic_cost_profile,
            generic_carbon_emissions_profile=generic_carbon_emissions_profile,
            generic_carbon_intensity_profile=generic_carbon_intensity_profile,
            generic_self_production_profile=generic_self_production_profile,
            load_profile_peak_timestamp=load_profile_peak_timestamp,
            load_profile_valley_timestamp=load_profile_valley_timestamp,
            grid_peak_timestamp=grid_peak_timestamp,
            generic_signal_start_timestamp=generic_signal_start_timestamp,
            generic_signal_end_timestamp=generic_signal_end_timestamp,
            low_generic_signal_start_timestamp=low_generic_signal_start_timestamp,
            low_generic_signal_end_timestamp=low_generic_signal_end_timestamp,
            medium_generic_signal_start_timestamp=medium_generic_signal_start_timestamp,
            medium_generic_signal_end_timestamp=medium_generic_signal_end_timestamp,
            high_generic_signal_start_timestamp=high_generic_signal_start_timestamp,
            high_generic_signal_end_timestamp=high_generic_signal_end_timestamp,
            high_price_start_timestamp=high_price_start_timestamp,
            high_price_end_timestamp=high_price_end_timestamp,
            high_emission_start_timestamp=high_emission_start_timestamp,
            high_emission_end_timestamp=high_emission_end_timestamp,
        )
        
        return np.nan, vs