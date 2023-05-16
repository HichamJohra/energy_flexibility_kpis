import datetime
from typing import List, Tuple, Union
import numpy as np
from energy_flexibility_kpis.base import Definition 
from energy_flexibility_kpis.enumerations import TemporalEvaluationWindow, TemporalResolution, SpatialResolution
from energy_flexibility_kpis.variable import VariableSet

class KPI(Definition):
    NAME = 'kpi'
    DEFINITION = __doc__
    UNIT = None
    CATEGORY = None
    RELEVANCE = None
    STAKEHOLDERS = None
    COMPLEXITY = None
    NEED_BASELINE = None
    TEMPORAL_EVALUATION_WINDOW = TemporalEvaluationWindow.UNSPECIFIED
    TEMPORAL_RESOLUTION = TemporalResolution.UNSPECIFIED
    SPATIAL_RESOLUTION = SpatialResolution.UNSPECIFIED
    DOE_FLEXIBILITY_CATEGORY = None
    PERFORMANCE_ASPECT = None

    def __init__(self) -> None:
        pass
    
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
        flexible_electric_power_profile: List[float] = None,
        flexible_electricity_consumption_profile: List[float] = None,
        flexible_natural_gas_consumption_profile: List[float] = None,
        generic_electric_power_profile: List[float] = None,
        generic_electricity_consumption_profile: List[float] = None,
        generic_natural_gas_consumption_profile: List[float] = None,
        load_profile_peak_timestamp: Union[int,datetime.datetime, str] = None,
        load_profile_valley_timestamp: Union[int,datetime.datetime, str] = None,
        grid_peak_timestamp: Union[int,datetime.datetime, str] = None,
        high_price_start_timestamp: Union[int,datetime.datetime, str] = None,
        high_price_end_timestamp: Union[int,datetime.datetime, str] = None,
        high_emission_start_timestamp: Union[int,datetime.datetime, str] = None,
        high_emission_end_timestamp: Union[int,datetime.datetime, str] = None,
    ) -> Tuple[Union[float, List[float]], VariableSet]:
        kwargs = locals()
        kwargs.pop('cls')
        vs = VariableSet(**kwargs)
        vs.validate_serial_variables()
        
        return np.nan, vs