import datetime
from typing import List, Union
import numpy as np
from scipy import integrate
from energy_flexibility_kpis.kpi.base import KPI
from energy_flexibility_kpis.enumerations import BaseUnit, Complexity, DOEFlexibilityCategory, KPICategory, PerformanceAspect, Relevance 
from energy_flexibility_kpis.enumerations import Stakeholder, TemporalEvaluationWindow,TemporalResolution, SpatialResolution
from energy_flexibility_kpis.unit import Unit

class CumulativeAverageThermalDiscomfort(KPI):
    """Defines the cumulative deviation of zone temperatures from upper and 
    lower comfort limits that are predefined within the test case FMU for 
    each zone, averaged over all zones."""

    NAME = 'cumulative average thermal discomfort'
    DEFINITION = __doc__
    UNIT = Unit(numerator=[BaseUnit.KELVIN, BaseUnit.HOUR])
    CATEGORY = KPICategory.EF_IMPACT_ON_IEQ
    RELEVANCE = Relevance.MEDIUM
    STAKEHOLDERS = [Stakeholder.BUILDING_OWNER, Stakeholder.BUILDING_OPERATOR]
    COMPLEXITY = Complexity.LOW
    NEED_BASELINE = True
    TEMPORAL_EVALUATION_WINDOW = TemporalEvaluationWindow.SINGLE_EVENT
    TEMPORAL_RESOLUTION = TemporalResolution.UNSPECIFIED
    SPATIAL_RESOLUTION = SpatialResolution.SINGLE_BUILDING
    DOE_FLEXIBILITY_CATEGORY = [DOEFlexibilityCategory.LOAD_SHIFTING, DOEFlexibilityCategory.LOAD_SHEDDING]
    PERFORMANCE_ASPECT = [PerformanceAspect.COMFORT]

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
        
        raise NotImplementedError('Variables are unclear.')
    
class CumulativeAverageIndoorAirQualityDiscomfort(KPI):
    """Defines the extent that the CO2 concentration levels in zones exceed 
    bounds of the acceptable concentration level, which are predefined within 
    the test case FMU for each zone, averaged over all zones."""

    NAME = 'cumulative average indoor air quality discomfort'
    DEFINITION = __doc__
    UNIT = Unit(numerator=[BaseUnit.PPM, BaseUnit.HOUR])
    CATEGORY = KPICategory.EF_IMPACT_ON_IEQ
    RELEVANCE = Relevance.MEDIUM
    STAKEHOLDERS = [Stakeholder.BUILDING_OWNER, Stakeholder.BUILDING_OPERATOR]
    COMPLEXITY = Complexity.LOW
    NEED_BASELINE = True
    TEMPORAL_EVALUATION_WINDOW = TemporalEvaluationWindow.SINGLE_EVENT
    TEMPORAL_RESOLUTION = TemporalResolution.UNSPECIFIED
    SPATIAL_RESOLUTION = SpatialResolution.SINGLE_BUILDING
    DOE_FLEXIBILITY_CATEGORY = [DOEFlexibilityCategory.LOAD_SHIFTING, DOEFlexibilityCategory.LOAD_SHEDDING]
    PERFORMANCE_ASPECT = [PerformanceAspect.COMFORT]

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
        
        raise NotImplementedError('Variables are unclear.')
    
class ImpactedDwellingsPercentage(KPI):
    """The percentage of the dwellings with a different duration of EHP activation 
    compared with the BaU case."""

    NAME = 'impacted dwellings percentage'
    DEFINITION = __doc__
    UNIT = Unit(numerator=[BaseUnit.DIMENSIONLESS])
    CATEGORY = KPICategory.EF_IMPACT_ON_IEQ
    RELEVANCE = Relevance.MEDIUM
    STAKEHOLDERS = [Stakeholder.GRID_OPERATOR, Stakeholder.DISTRIBUTION_SYSTEM_OPERATOR, Stakeholder.TRANSMISSION_SYSTEM_OPERATOR]
    COMPLEXITY = Complexity.LOW
    NEED_BASELINE = True
    TEMPORAL_EVALUATION_WINDOW = TemporalEvaluationWindow.MULTIPLE_EVENTS
    TEMPORAL_RESOLUTION = TemporalResolution.UNSPECIFIED
    SPATIAL_RESOLUTION = SpatialResolution.BUILDING_CLUSTER
    DOE_FLEXIBILITY_CATEGORY = [DOEFlexibilityCategory.LOAD_SHIFTING, DOEFlexibilityCategory.LOAD_SHEDDING]
    PERFORMANCE_ASPECT = [PerformanceAspect.COMFORT]

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
        
        raise NotImplementedError('Variables are unclear.')
    
class AverageDisruptionDuration(KPI):
    """Measure the average change of EHP activation time across the service deployment period."""

    NAME = 'average disruption duration'
    DEFINITION = __doc__
    UNIT = Unit(numerator=[BaseUnit.MINUTE])
    CATEGORY = KPICategory.EF_IMPACT_ON_IEQ
    RELEVANCE = Relevance.MEDIUM
    STAKEHOLDERS = [Stakeholder.GRID_OPERATOR, Stakeholder.DISTRIBUTION_SYSTEM_OPERATOR, Stakeholder.TRANSMISSION_SYSTEM_OPERATOR]
    COMPLEXITY = Complexity.LOW
    NEED_BASELINE = True
    TEMPORAL_EVALUATION_WINDOW = TemporalEvaluationWindow.MULTIPLE_EVENTS
    TEMPORAL_RESOLUTION = TemporalResolution.UNSPECIFIED
    SPATIAL_RESOLUTION = SpatialResolution.BUILDING_CLUSTER
    DOE_FLEXIBILITY_CATEGORY = [DOEFlexibilityCategory.LOAD_SHIFTING, DOEFlexibilityCategory.LOAD_SHEDDING]
    PERFORMANCE_ASPECT = [PerformanceAspect.COMFORT]

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
        
        raise NotImplementedError('Variables are unclear.')