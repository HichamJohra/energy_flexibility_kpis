import datetime
from typing import List, Union
import pandas as pd
from energy_flexibility_kpis.kpi.base import KPI
from energy_flexibility_kpis.enumerations import BaseUnit, Complexity, DOEFlexibilityCategory, KPICategory, PerformanceAspect, Relevance 
from energy_flexibility_kpis.enumerations import Stakeholder, TemporalEvaluationWindow,TemporalResolution, SpatialResolution
from energy_flexibility_kpis.unit import Unit
from energy_flexibility_kpis.variable import Variable

class EnergyDeviationForPeakShaving(KPI):
    """Peak-shaving capacity."""

    NAME = 'energy deviation from peak shaving'
    DEFINITION = __doc__
    UNIT = Unit(numerator=[BaseUnit.KWH])
    CATEGORY = KPICategory.EF_ENERGY_OR_AVERAGE_POWER_LOAD_SHEDDING
    RELEVANCE = Relevance.HIGH
    STAKEHOLDERS = [Stakeholder.BUILDING_OWNER, Stakeholder.GRID_OPERATOR]
    COMPLEXITY = Complexity.LOW
    NEED_BASELINE = True
    TEMPORAL_EVALUATION_WINDOW = TemporalEvaluationWindow.SINGLE_EVENT
    TEMPORAL_RESOLUTION = TemporalResolution.UNSPECIFIED
    SPATIAL_RESOLUTION = SpatialResolution.UNSPECIFIED
    DOE_FLEXIBILITY_CATEGORY = [DOEFlexibilityCategory.LOAD_SHEDDING]
    PERFORMANCE_ASPECT = [PerformanceAspect.ENERGY]

    def __init__(self):
        super().__init__()

    @classmethod
    def calculate(
        cls,
        baseline_electric_power_profile: Union[Variable, List[float]], 
        flexible_electric_power_profile: Union[Variable, List[float]],
        timestamps: Union[Variable, List[int], List[datetime.datetime], List[str]] = None,
        evaluation_start_timestamp: Union[Variable, int,datetime.datetime, str] = None,
        evaluation_end_timestamp: Union[Variable, int,datetime.datetime, str] = None,
    ) -> float:
        _, vs = super().calculate(
            baseline_electric_power_profile=baseline_electric_power_profile,
            flexible_electric_power_profile=flexible_electric_power_profile,
            timestamps=timestamps,
            evaluation_start_timestamp=evaluation_start_timestamp,
            evaluation_end_timestamp=evaluation_end_timestamp,
        )

        value = (
            vs.flexible_electric_power_profile.value[vs.evaluation_mask] 
                - vs.baseline_electric_power_profile.value[vs.evaluation_mask]
        ).mean()*len(vs.evaluation_mask)

        return value
    
class AverageLoadReduction(KPI):
    """Average load reduction during the demand response event (peak load shaving) by number of buildings."""

    NAME = 'average load reduction'
    DEFINITION = __doc__
    UNIT = Unit(numerator=[BaseUnit.KW])
    CATEGORY = KPICategory.EF_ENERGY_OR_AVERAGE_POWER_LOAD_SHEDDING
    RELEVANCE = Relevance.HIGH
    STAKEHOLDERS = [Stakeholder.DISTRIBUTION_SYSTEM_OPERATOR, Stakeholder.TRANSMISSION_SYSTEM_OPERATOR]
    COMPLEXITY = Complexity.LOW
    NEED_BASELINE = True
    TEMPORAL_EVALUATION_WINDOW = TemporalEvaluationWindow.SINGLE_EVENT
    TEMPORAL_RESOLUTION = TemporalResolution.UNSPECIFIED
    SPATIAL_RESOLUTION = SpatialResolution.BUILDING_CLUSTER
    DOE_FLEXIBILITY_CATEGORY = [DOEFlexibilityCategory.LOAD_SHEDDING]
    PERFORMANCE_ASPECT = [PerformanceAspect.POWER]

    def __init__(self):
        super().__init__()

    @classmethod
    def calculate(
        cls,
        baseline_electric_power_profile: Union[Variable, List[float]], 
        flexible_electric_power_profile: Union[Variable, List[float]],
        generic_resource_count: int,
        timestamps: Union[Variable, List[int], List[datetime.datetime], List[str]] = None,
        evaluation_start_timestamp: Union[Variable, int,datetime.datetime, str] = None,
        evaluation_end_timestamp: Union[Variable, int,datetime.datetime, str] = None,
    ) -> float:
        _, vs = super().calculate(
            baseline_electric_power_profile=baseline_electric_power_profile,
            flexible_electric_power_profile=flexible_electric_power_profile,
            generic_resource_count=generic_resource_count,
            timestamps=timestamps,
            evaluation_start_timestamp=evaluation_start_timestamp,
            evaluation_end_timestamp=evaluation_end_timestamp,
        )
        
        assert len(vs.evaluation_mask) > 1, 'The evaluation period must be > 1 timestep'
        
        value = (
            vs.baseline_electric_power_profile.value[vs.evaluation_mask] 
                - vs.flexible_electric_power_profile.value[vs.evaluation_mask]
        )[1:].sum()/(vs.generic_resource_count.value*(len(vs.evaluation_mask) - 1))

        return value
    
class BuildingEnergyFlexibilityIndex(KPI):
    """Calculating the average power reduction/increase by considering the difference between the energy used by a 
    reference load profile (“business as usual”) scenario (Pref) and the energy used in a new, “flexibility” scenario 
    (Pflex). Dividing by the duration of the event."""

    NAME = 'building energy flexibility index'
    DEFINITION = __doc__
    UNIT = Unit(numerator=[BaseUnit.KW])
    CATEGORY = KPICategory.EF_ENERGY_OR_AVERAGE_POWER_LOAD_SHEDDING
    RELEVANCE = Relevance.HIGH
    STAKEHOLDERS = [Stakeholder.OCCUPANT, Stakeholder.BUILDING_OWNER]
    COMPLEXITY = Complexity.MEDIUM
    NEED_BASELINE = True
    TEMPORAL_EVALUATION_WINDOW = TemporalEvaluationWindow.SINGLE_EVENT
    TEMPORAL_RESOLUTION = TemporalResolution.UNSPECIFIED
    SPATIAL_RESOLUTION = SpatialResolution.UNSPECIFIED
    DOE_FLEXIBILITY_CATEGORY = [DOEFlexibilityCategory.LOAD_SHEDDING]
    PERFORMANCE_ASPECT = [PerformanceAspect.POWER]

    def __init__(self):
        super().__init__()

    @classmethod
    def calculate(
        cls,
        baseline_electric_power_profile: Union[Variable, List[float]], 
        flexible_electric_power_profile: Union[Variable, List[float]],
        timestamps: Union[Variable, List[int], List[datetime.datetime], List[str]] = None,
        evaluation_start_timestamp: Union[Variable, int,datetime.datetime, str] = None,
        evaluation_end_timestamp: Union[Variable, int,datetime.datetime, str] = None,
    ) -> float:
        _, vs = super().calculate(
            baseline_electric_power_profile=baseline_electric_power_profile,
            flexible_electric_power_profile=flexible_electric_power_profile,
            timestamps=timestamps,
            evaluation_start_timestamp=evaluation_start_timestamp,
            evaluation_end_timestamp=evaluation_end_timestamp,
        )
        
        value = (
            vs.baseline_electric_power_profile.value[vs.evaluation_mask] 
                - vs.flexible_electric_power_profile.value[vs.evaluation_mask]
        ).sum()/len(vs.evaluation_mask)

        return value
    
class DimensionlessPeakShaving(KPI):
    """Represents the energy reduction percentage of the cooling system during the downward flexibility period."""

    NAME = 'dimensionless peak shaving'
    DEFINITION = __doc__
    UNIT = Unit(numerator=[BaseUnit.DIMENSIONLESS])
    CATEGORY = KPICategory.EF_ENERGY_OR_AVERAGE_POWER_LOAD_SHEDDING
    RELEVANCE = Relevance.LOW
    STAKEHOLDERS = [Stakeholder.GRID_OPERATOR, Stakeholder.BUILDING_MANAGER]
    COMPLEXITY = Complexity.LOW
    NEED_BASELINE = True
    TEMPORAL_EVALUATION_WINDOW = TemporalEvaluationWindow.SINGLE_EVENT
    TEMPORAL_RESOLUTION = TemporalResolution.UNSPECIFIED
    SPATIAL_RESOLUTION = SpatialResolution.UNSPECIFIED
    DOE_FLEXIBILITY_CATEGORY = [DOEFlexibilityCategory.LOAD_SHEDDING]
    PERFORMANCE_ASPECT = [PerformanceAspect.POWER, PerformanceAspect.ENERGY]

    def __init__(self):
        super().__init__()

    @classmethod
    def calculate(
        cls,
        baseline_electric_power_profile: Union[Variable, List[float]], 
        flexible_electric_power_profile: Union[Variable, List[float]],
        timestamps: Union[Variable, List[int], List[datetime.datetime], List[str]] = None,
        evaluation_start_timestamp: Union[Variable, int,datetime.datetime, str] = None,
        evaluation_end_timestamp: Union[Variable, int,datetime.datetime, str] = None,
    ) -> float:
        _, vs = super().calculate(
            baseline_electric_power_profile=baseline_electric_power_profile,
            flexible_electric_power_profile=flexible_electric_power_profile,
            timestamps=timestamps,
            evaluation_start_timestamp=evaluation_start_timestamp,
            evaluation_end_timestamp=evaluation_end_timestamp,
        )

        delta_p_downward = (
            vs.baseline_electric_power_profile.value[vs.evaluation_mask]
                - vs.flexible_electric_power_profile.value[vs.evaluation_mask]
        ).sum()/len(vs.evaluation_mask)
        q_peak_shaving = delta_p_downward*len(vs.evaluation_mask)
        value = q_peak_shaving/vs.baseline_electric_power_profile.value[vs.evaluation_mask].sum()

        return value
    
class LoadFactor(KPI):
    """Dividing the average load to the peak load in a specified period."""

    NAME = 'load factor'
    DEFINITION = __doc__
    UNIT = Unit(numerator=[BaseUnit.DIMENSIONLESS])
    CATEGORY = KPICategory.EF_ENERGY_OR_AVERAGE_POWER_LOAD_SHEDDING
    RELEVANCE = Relevance.LOW
    STAKEHOLDERS = [Stakeholder.BUILDING_OWNER, Stakeholder.POWER_SUPPLIER]
    COMPLEXITY = Complexity.LOW
    NEED_BASELINE = False
    TEMPORAL_EVALUATION_WINDOW = TemporalEvaluationWindow.SINGLE_EVENT
    TEMPORAL_RESOLUTION = TemporalResolution.UNSPECIFIED
    SPATIAL_RESOLUTION = SpatialResolution.UNSPECIFIED
    DOE_FLEXIBILITY_CATEGORY = [DOEFlexibilityCategory.LOAD_SHEDDING]
    PERFORMANCE_ASPECT = [PerformanceAspect.POWER, PerformanceAspect.ENERGY]

    def __init__(self):
        super().__init__()

    @classmethod
    def calculate(
        cls,
        generic_electric_power_profile: Union[Variable, List[float]],
        timestamps: Union[Variable, List[int], List[datetime.datetime], List[str]] = None,
        evaluation_start_timestamp: Union[Variable, int,datetime.datetime, str] = None,
        evaluation_end_timestamp: Union[Variable, int,datetime.datetime, str] = None,
    ) -> float:
        _, vs = super().calculate(
            generic_electric_power_profile=generic_electric_power_profile,
            timestamps=timestamps,
            evaluation_start_timestamp=evaluation_start_timestamp,
            evaluation_end_timestamp=evaluation_end_timestamp,
        )

        value = vs.generic_electric_power_profile[vs.evaluation_mask].mean()\
            /vs.generic_electric_power_profile[vs.evaluation_mask].max()

        return value
    
class AnnualAverageDailyLoadVariation(KPI):
    """An indicator expressing the overall level of load variability in buildings quantified using the accumulated sum of daily load variations relative to the annual heating energy use (unit: unitless). Knowledge about load variations is of interest to."""

    NAME = 'annual average daily load variation'
    DEFINITION = __doc__
    UNIT = Unit(numerator=[BaseUnit.DIMENSIONLESS])
    CATEGORY = KPICategory.EF_ENERGY_OR_AVERAGE_POWER_LOAD_SHEDDING
    RELEVANCE = Relevance.LOW
    STAKEHOLDERS = [Stakeholder.UTILITY_COMPANY]
    COMPLEXITY = Complexity.MEDIUM
    NEED_BASELINE = False
    TEMPORAL_EVALUATION_WINDOW = TemporalEvaluationWindow.WHOLE_YEAR
    TEMPORAL_RESOLUTION = TemporalResolution.HOURLY
    SPATIAL_RESOLUTION = SpatialResolution.UNSPECIFIED
    DOE_FLEXIBILITY_CATEGORY = [DOEFlexibilityCategory.LOAD_SHEDDING]
    PERFORMANCE_ASPECT = [PerformanceAspect.ENERGY]

    def __init__(self):
        super().__init__()

    @classmethod
    def calculate(
        cls,
        generic_electric_power_profile: Union[Variable, List[float]],
        timestamps: Union[Variable, List[int], List[datetime.datetime], List[str]],
        evaluation_start_timestamp: Union[Variable, int,datetime.datetime, str] = None,
        evaluation_end_timestamp: Union[Variable, int,datetime.datetime, str] = None,
    ) -> List[float]:
        _, vs = super().calculate(
            generic_electric_power_profile=generic_electric_power_profile,
            timestamps=timestamps,
            evaluation_start_timestamp=evaluation_start_timestamp,
            evaluation_end_timestamp=evaluation_end_timestamp,
        )

        # get timestamp variables
        data = pd.DataFrame({
            'timestamp': vs.timestamps.value[vs.evaluation_mask],
            'generic_electric_power_profile': vs.generic_electric_power_profile[vs.evaluation_mask]
        })
        data['year'] = data['timestamp'].dt.year
        data['day_of_year'] = data['timestamp'].dt.day_of_year
        data['hour'] = data['timestamp'].dt.hour
        
        # calculate annual, daily and hour averge loads
        yearly = data.groupby(['year'])[['generic_electric_power_profile']].mean()
        yearly.columns = ['yearly']
        daily = data.groupby(['year', 'day_of_year'])[['generic_electric_power_profile']].mean()
        daily.columns = ['daily']
        hourly = data.groupby(['year', 'day_of_year', 'hour'])[['generic_electric_power_profile']].mean()
        hourly.columns = ['hourly']
        
        # calculate KPI
        data = daily.reset_index().merge(hourly.reset_index(), on=['year', 'day_of_year'])
        data['numerator'] = (data['hourly'] - data['daily']).abs()
        data['hour_count'] = 1
        data = data.groupby(['year'])[['numerator', 'hour_count']].sum().reset_index()
        data['numerator'] *= 0.5
        data = data.merge(yearly.reset_index(), on=['year'])
        value = data['numerator']*100.0/(data['hour_count']*data['yearly'])
        value = value.tolist()

        return value
    
class PriceResponsiveness(KPI):
    """t_test for testing power shaving significance between tested building cluster conducting DR and reference 
    building cluster without DR event."""

    NAME = 'price responsiveness'
    DEFINITION = __doc__
    UNIT = Unit(numerator=[BaseUnit.DIMENSIONLESS])
    CATEGORY = KPICategory.EF_ENERGY_OR_AVERAGE_POWER_LOAD_SHEDDING
    RELEVANCE = Relevance.MEDIUM
    STAKEHOLDERS = [Stakeholder.DISTRIBUTION_SYSTEM_OPERATOR, Stakeholder.BUILDING_OWNER]
    COMPLEXITY = Complexity.HIGH
    NEED_BASELINE = True
    TEMPORAL_EVALUATION_WINDOW = TemporalEvaluationWindow.SINGLE_EVENT
    TEMPORAL_RESOLUTION = TemporalResolution.UNSPECIFIED
    SPATIAL_RESOLUTION = SpatialResolution.BUILDING_CLUSTER
    DOE_FLEXIBILITY_CATEGORY = [DOEFlexibilityCategory.LOAD_SHIFTING, DOEFlexibilityCategory.LOAD_SHEDDING]
    PERFORMANCE_ASPECT = [PerformanceAspect.POWER, PerformanceAspect.COST]

    def __init__(self):
        super().__init__()

    @classmethod
    def calculate(
        cls,
        generic_electric_power_profile: Union[Variable, List[float]],
        timestamps: Union[Variable, List[int], List[datetime.datetime], List[str]],
        evaluation_start_timestamp: Union[Variable, int,datetime.datetime, str] = None,
        evaluation_end_timestamp: Union[Variable, int,datetime.datetime, str] = None,
    ) -> List[float]:
        _, vs = super().calculate(
            generic_electric_power_profile=generic_electric_power_profile,
            timestamps=timestamps,
            evaluation_start_timestamp=evaluation_start_timestamp,
            evaluation_end_timestamp=evaluation_end_timestamp,
        )

        # get timestamp variables
        data = pd.DataFrame({
            'timestamp': vs.timestamps.value[vs.evaluation_mask],
            'generic_electric_power_profile': vs.generic_electric_power_profile[vs.evaluation_mask]
        })
        data['year'] = data['timestamp'].dt.year
        data['day_of_year'] = data['timestamp'].dt.day_of_year
        data['hour'] = data['timestamp'].dt.hour
        
        # calculate annual, daily and hour averge loads
        yearly = data.groupby(['year'])[['generic_electric_power_profile']].mean()
        yearly.columns = ['yearly']
        daily = data.groupby(['year', 'day_of_year'])[['generic_electric_power_profile']].mean()
        daily.columns = ['daily']
        hourly = data.groupby(['year', 'day_of_year', 'hour'])[['generic_electric_power_profile']].mean()
        hourly.columns = ['hourly']
        
        # calculate KPI
        data = daily.reset_index().merge(hourly.reset_index(), on=['year', 'day_of_year'])
        data['numerator'] = (data['hourly'] - data['daily']).abs()
        data['hour_count'] = 1
        data = data.groupby(['year'])[['numerator', 'hour_count']].sum().reset_index()
        data['numerator'] *= 0.5
        data = data.merge(yearly.reset_index(), on=['year'])
        value = data['numerator']*100.0/(data['hour_count']*data['yearly'])
        value = value.tolist()

        return value
    
class FlexibleTimeDuration(KPI):
    """The duration that a building could reduce or increase its power demand without impacting normal operations."""

    def __init__(*args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def calculate(self) -> Union[float, List[float]]:
        _ = super().calculate()
        raise NotImplementedError
    
class FlexibilityDensity(KPI):
    """Demand response potential of a given spatial area as a function of response potential of batteries, heat pumps, 
    thermal energy storages and electric vehicles."""

    def __init__(*args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def calculate(self) -> Union[float, List[float]]:
        _ = super().calculate()
        raise NotImplementedError
    
class AverageDownwardPowerDeviation(KPI):
    """Average power deviation during the downward modulation period."""

    def __init__(*args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def calculate(self) -> Union[float, List[float]]:
        _ = super().calculate()
        raise NotImplementedError