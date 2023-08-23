import datetime
from typing import List, Union
from scipy import integrate
from energy_flexibility_kpis.kpi.base import KPI
from energy_flexibility_kpis.enumerations import BaseUnit, Complexity, DOEFlexibilityCategory, KPICategory, PerformanceAspect, Relevance 
from energy_flexibility_kpis.enumerations import Stakeholder, TemporalEvaluationWindow,TemporalResolution, SpatialResolution
from energy_flexibility_kpis.unit import Unit

class CapacityOfADR(KPI):
    """The amount of energy that can be added to or removed from the storage system during an ADR 
    action (up/down-flex)."""

    NAME = 'capacity of ADR'
    DEFINITION = __doc__
    UNIT = Unit(numerator=[BaseUnit.KWH])
    CATEGORY = KPICategory.EF_ENERGY_STORAGE_CAPABILITY
    RELEVANCE = Relevance.HIGH
    STAKEHOLDERS = [Stakeholder.BUILDING_OPERATOR, Stakeholder.TRANSMISSION_SYSTEM_OPERATOR]
    COMPLEXITY = Complexity.LOW
    NEED_BASELINE = True
    TEMPORAL_EVALUATION_WINDOW = TemporalEvaluationWindow.SINGLE_EVENT
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
        timestamps: Union[List[int], List[datetime.datetime], List[str]],
        evaluation_start_timestamp: Union[int, datetime.datetime, str] = None,
        evaluation_end_timestamp: Union[int, datetime.datetime, str] = None,
    ) -> float:
        """Assumes timestamps are datetime values."""

        _, vs = super().calculate(
            timestamps=timestamps,
            baseline_electric_power_profile=baseline_electric_power_profile,
            flexible_electric_power_profile=flexible_electric_power_profile,
            evaluation_start_timestamp=evaluation_start_timestamp,
            evaluation_end_timestamp=evaluation_end_timestamp,
        )
        
        profile = vs.flexible_electric_power_profile.value[vs.evaluation_mask] - vs.baseline_electric_power_profile.value[vs.evaluation_mask]
        dx = vs.get_temporal_resolution(BaseUnit.HOUR, value=vs.timestamps.value[vs.evaluation_mask])
        value = integrate.simpson(profile, dx=dx)

        return value
    
class EnergyEfficiencyOfDemandResponseAction(KPI):
    """The fraction of the energy stored during the ADR event that can be used subsequently to reduce 
    the power needed to maintain thermal comfort."""

    NAME = 'energy efficiency of demand response action'
    DEFINITION = __doc__
    UNIT = Unit(numerator=[BaseUnit.DIMENSIONLESS])
    CATEGORY = KPICategory.EF_ENERGY_STORAGE_CAPABILITY
    RELEVANCE = Relevance.HIGH
    STAKEHOLDERS = [Stakeholder.BUILDING_OPERATOR, Stakeholder.TRANSMISSION_SYSTEM_OPERATOR]
    COMPLEXITY = Complexity.LOW
    NEED_BASELINE = True
    TEMPORAL_EVALUATION_WINDOW = TemporalEvaluationWindow.SINGLE_EVENT
    TEMPORAL_RESOLUTION = TemporalResolution.UNSPECIFIED
    SPATIAL_RESOLUTION = SpatialResolution.UNSPECIFIED
    DOE_FLEXIBILITY_CATEGORY = [DOEFlexibilityCategory.LOAD_SHIFTING]
    PERFORMANCE_ASPECT = [PerformanceAspect.ENERGY]

    def __init__(self):
        super().__init__()

    @classmethod
    def calculate(
        cls,
        baseline_electric_power_profile: List[float],
        flexible_electric_power_profile: List[float],
        generic_signal_start_timestamp: Union[int, datetime.datetime, str],
        generic_signal_end_timestamp: Union[int, datetime.datetime, str],
        timestamps: Union[List[int], List[datetime.datetime], List[str]],
        evaluation_start_timestamp: Union[int, datetime.datetime, str] = None,
        evaluation_end_timestamp: Union[int, datetime.datetime, str] = None,
    ) -> float:
        """Assumes timestamps is in hours when calculating integral."""

        _, vs = super().calculate(
            timestamps=timestamps,
            baseline_electric_power_profile=baseline_electric_power_profile,
            flexible_electric_power_profile=flexible_electric_power_profile,
            generic_signal_start_timestamp=generic_signal_start_timestamp,
            generic_signal_end_timestamp=generic_signal_end_timestamp,
            evaluation_start_timestamp=evaluation_start_timestamp,
            evaluation_end_timestamp=evaluation_end_timestamp,
        )

        profile = vs.flexible_electric_power_profile.value[vs.evaluation_mask] - vs.baseline_electric_power_profile.value[vs.evaluation_mask]
        adr_mask = vs.evaluation_mask\
            & (vs.timestamps.value >= vs.generic_signal_start_timestamp.value)\
                & (vs.timestamps.value <= vs.generic_signal_end_timestamp.value)
        adr_profile = vs.flexible_electric_power_profile.value[adr_mask] - vs.baseline_electric_power_profile.value[adr_mask]
        dx = vs.get_temporal_resolution(BaseUnit.HOUR, vs.timestamps.value[vs.evaluation_mask])
        adr_dx = vs.get_temporal_resolution(BaseUnit.HOUR, vs.timestamps.value[adr_mask])
        value = 1 - (integrate.simpson(profile, dx=dx)/integrate.simpson(adr_profile, dx=adr_dx))

        return value
    
class AvailableFlexibleEnergy(KPI):
    """Amount of (thermal) energy stored in a building system (indoor environment and/or storage tank) 
    that can be used for load shifting."""

    NAME = 'available flexible energy'
    DEFINITION = __doc__
    UNIT = Unit(numerator=[BaseUnit.KWH])
    CATEGORY = KPICategory.EF_ENERGY_STORAGE_CAPABILITY
    RELEVANCE = Relevance.MEDIUM
    STAKEHOLDERS = [Stakeholder.DISTRIBUTION_SYSTEM_OPERATOR, Stakeholder.TRANSMISSION_SYSTEM_OPERATOR]
    COMPLEXITY = Complexity.LOW
    NEED_BASELINE = False
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
        timestamps: Union[List[int], List[datetime.datetime], List[str]] = None,
        evaluation_start_timestamp: Union[int, datetime.datetime, str] = None,
        evaluation_end_timestamp: Union[int, datetime.datetime, str] = None,
    ) -> float:
        _, vs = super().calculate(
            timestamps=timestamps,
            evaluation_start_timestamp=evaluation_start_timestamp,
            evaluation_end_timestamp=evaluation_end_timestamp,
        )
        
        raise NotImplementedError('Cannot find how equation is used is paper')