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
    def calculate(cls, **kwargs) -> Tuple[Union[float, List[float]], VariableSet]:
        vs = VariableSet(**kwargs)
        vs.validate_serial_variables()
        
        return np.nan, vs