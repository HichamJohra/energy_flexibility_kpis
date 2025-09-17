import datetime
import math
from typing import Any, List, Mapping, Union
import numpy as np
import pandas as pd
from energy_flexibility_kpis.base import Definition
from energy_flexibility_kpis.enumerations import BaseUnit, OperationCondition, ValueType
from energy_flexibility_kpis.primitive_type import DefaultPrimitiveType, PrimitiveType
from energy_flexibility_kpis.unit import Unit

class Variable(Definition):
    def __init__(
            self, name: str, definition: str, primitive_type: PrimitiveType, value_type: ValueType, 
            operation_condition: OperationCondition = None, value: Union[str, int, float, bool, datetime.datetime, list, np.ndarray] = None, unit: Unit = None, 
            efont_uri: str = None, brick_uri: str = None
        ):
        super().__init__()
        self.name = name
        self.definition = definition
        self.primitive_type = primitive_type
        self.value_type = value_type
        self.value = value
        self.unit = unit
        self.operation_condition = operation_condition
        self.efont_uri = efont_uri
        self.brick_uri = brick_uri

    @property
    def unit(self) -> Unit:
        self.primitive_type.unit if self.__unit is None else self.__unit

    @property
    def value(self) -> np.ndarray:
        return self.__value
    
    @property
    def operation_condition(self) -> OperationCondition:
        return self.__operation_condition
    
    @property
    def snake_case_name(self) -> str:
        return self.name.strip().replace(' ', '_')
    
    def info(self) -> Mapping[str, Any]:
        return {
            'name': self.name,
            'snake_case_name': self.snake_case_name,
            'definition': self.definition,
            'primitive_type': self.primitive_type.info(),
            'value_type': self.value_type.value,
            'unit': str(self.unit),
            'operation_condition': self.operation_condition.value,
            'efont_uri': self.efont_uri,
            'brick_uri': self.brick_uri
        }

    @unit.setter
    def unit(self, value: Unit):
        self.__unit = value

    @value.setter
    def value(self, value: Union[str, int, float, bool, datetime.datetime, list, np.ndarray]):
        value_type_error_message = f'The variable {self.snake_case_name} is a {self.value_type}'\
            f' value type and must be one of the following types: {[v.__name__ for v in self.value_type.value]}.'

        if value is None or isinstance(value, pd._libs.tslibs.nattype.NaTType):
            pass
        
        elif (isinstance(value, float) and math.isnan(value)) or isinstance(value, pd._libs.tslibs.nattype.NaTType):
            value = None

        elif self.value_type == ValueType.SINGLE:
            assert isinstance(value, tuple(self.value_type.value)), value_type_error_message
            value = np.array(value, dtype=type(value))
        
        elif self.value_type == ValueType.SERIAL:
            assert isinstance(value, tuple(self.value_type.value)), value_type_error_message
            value = np.array(value, dtype=type(value[0]))
           
        else:
            raise Exception(f'Unknown value_type: {self.value_type}')

        self.__value = value

    @operation_condition.setter
    def operation_condition(self, value: OperationCondition):
        self.__operation_condition = OperationCondition.GENERIC if value is None else value

class DateTimeVariable(Variable):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @Variable.value.setter
    def value(self, value: Union[str, datetime.datetime, int, list]):
        # if it is an integer, then it is assumed to be a timestep not a timestamp
        if (self.value_type == ValueType.SINGLE and not isinstance(value, int))\
            or (self.value_type == ValueType.SERIAL\
                and (not isinstance(value, list) or not isinstance(value[0], int))
            ):
            value = pd.to_datetime(value)
            
            try:
                value = value.tolist()
            except AttributeError:
                pass
        
        else:
            pass
        
        Variable.value.fset(self, value)

    def get_resolution(self, unit: BaseUnit, value: List[datetime.datetime] = None) -> float:
        """Estimates time step resolution in specified time unit."""

        assert isinstance(self.value[0], datetime.datetime),\
            'Cannot infer resolution of non-datetime timestamps'
        
        resolution = None
        value = self.value if value is None else value
        timestamps = pd.to_datetime(value)
        resolutions = timestamps.to_series().diff()
        minimum_resolution = resolutions.min().total_seconds()
        maximum_resolution = resolutions.max().total_seconds()

        assert minimum_resolution == maximum_resolution,\
            f'Discontinuous time series. Minimum time interval ({minimum_resolution}s)'\
                f'and maximum time interval ({maximum_resolution}s) are not equal.'
        
        if unit == BaseUnit.MILLISECOND:
            resolution = minimum_resolution*1000.0
        
        elif unit == BaseUnit.SECOND:
            resolution = minimum_resolution

        elif unit == BaseUnit.MINUTE:
            resolution = minimum_resolution/60.0

        elif unit == BaseUnit.HOUR:
            resolution = minimum_resolution/3600.0

        else:
            raise Exception(f'Unknown unit: {unit}')

        return resolution

class DefaultVariableMetaClass(type):
    def __init__(cls, *args, **kwargs) -> None:
        pass
    
    @property
    def availability(cls) -> Variable:
        return Variable(
            name='availability',
            definition='Equipment availability mask.',
            primitive_type=DefaultPrimitiveType.unspecified,
            value_type=ValueType.SERIAL,
        )

    @property
    def zone_temperature_profile(cls) -> Variable:
        return Variable(
            name='zone_temperature_profile',
            definition='A time series data points of zone_temperature_profile.',
            primitive_type=DefaultPrimitiveType.temperature,
            value_type=ValueType.SERIAL,
        )
    
    @property
    def cooling_setpoints(cls) -> Variable:
        return Variable(
            name='cooling_setpoints',
            definition='A time series data points of cooling_setpoints.',
            primitive_type=DefaultPrimitiveType.temperature,
            value_type=ValueType.SERIAL,
        )
    
    @property
    def heating_setpoints(cls) -> Variable:
        return Variable(
            name='heating_setpoints',
            definition='A time series data points of heating_setpoints.',
            primitive_type=DefaultPrimitiveType.temperature,
            value_type=ValueType.SERIAL,
        )
    
    @property
    def baseline_electric_power_profile(cls) -> Variable:
        return Variable(
            name='baseline electric power profile',
            definition='A time series data points of electric power demand acquired in baseline operation scenario.',
            primitive_type=DefaultPrimitiveType.power_demand,
            value_type=ValueType.SERIAL,
            operation_condition=OperationCondition.BASELINE,
        )
    
    @property
    def baseline_electricity_consumption_profile(cls) -> Variable:
        return Variable(
            name='baseline electricity consumption profile',
            definition='A time series data points of electricity consumption acquired in baseline operation scenario.',
            primitive_type=DefaultPrimitiveType.energy_consumption,
            value_type=ValueType.SERIAL,
            operation_condition=OperationCondition.BASELINE,
        )
    
    @property
    def baseline_natural_gas_consumption_profile(cls) -> Variable:
        return Variable(
            name='baseline natural gas consumption profile',
            definition='A time series data points of natural gas consumption acquired in baseline operation scenario.',
            primitive_type=DefaultPrimitiveType.energy_consumption,
            value_type=ValueType.SERIAL,
            operation_condition=OperationCondition.BASELINE,
        )
    
    @property
    def baseline_cost_profile(cls) -> Variable:
        return Variable(
            name='baseline cost profile',
            definition='A time series data points of energy cost acquired in baseline operation scenario.',
            primitive_type=DefaultPrimitiveType.operation_cost,
            value_type=ValueType.SERIAL,
            operation_condition=OperationCondition.BASELINE,
        )
    
    @property
    def baseline_carbon_emissions_profile(cls) -> Variable:
        return Variable(
            name='baseline carbon emissions profile',
            definition='A time series data points of energy carbon emissions acquired in baseline operation scenario.',
            primitive_type=DefaultPrimitiveType.carbon_emission,
            value_type=ValueType.SERIAL,
            operation_condition=OperationCondition.BASELINE,
        )
    
    @property
    def baseline_carbon_intensity_profile(cls) -> Variable:
        return Variable(
            name='baseline carbon intensity profile',
            definition='A time series data points of energy carbon intensity acquired in baseline operation scenario.',
            primitive_type=DefaultPrimitiveType.carbon_emission_factor,
            value_type=ValueType.SERIAL,
            operation_condition=OperationCondition.BASELINE,
        )
    
    @property
    def baseline_self_production_profile(cls) -> Variable:
        return Variable(
            name='baseline self production profile',
            definition='A time series data points of self-produced acquired in baseline operation scenario.',
            primitive_type=DefaultPrimitiveType.power_demand,
            value_type=ValueType.SERIAL,
            operation_condition=OperationCondition.BASELINE,
        )
    
    @property
    def flexible_electric_power_profile(cls) -> Variable:
        return Variable(
            name='flexible electric power profile',
            definition='A time series data points of electric power demand acquired in flexible operation scenario.',
            primitive_type=DefaultPrimitiveType.power_demand,
            value_type=ValueType.SERIAL,
            operation_condition=OperationCondition.FLEXIBLE,
        )
    
    @property
    def flexible_electricity_consumption_profile(cls) -> Variable:
        return Variable(
            name='flexible electricity consumption profile',
            definition='A time series data points of electricity consumption acquired in flexible operation scenario.',
            primitive_type=DefaultPrimitiveType.energy_consumption,
            value_type=ValueType.SERIAL,
            operation_condition=OperationCondition.FLEXIBLE,
        )
    
    @property
    def flexible_natural_gas_consumption_profile(cls) -> Variable:
        return Variable(
            name='flexible natural gas consumption profile',
            definition='A time series data points of natural gas consumption acquired in flexible operation scenario.',
            primitive_type=DefaultPrimitiveType.energy_consumption,
            value_type=ValueType.SERIAL,
            operation_condition=OperationCondition.FLEXIBLE,
        )
    
    @property
    def flexible_cost_profile(cls) -> Variable:
        return Variable(
            name='flexible cost profile',
            definition='A time series data points of energy cost acquired in flexible operation scenario.',
            primitive_type=DefaultPrimitiveType.operation_cost,
            value_type=ValueType.SERIAL,
            operation_condition=OperationCondition.FLEXIBLE,
        )
    
    @property
    def flexible_carbon_emissions_profile(cls) -> Variable:
        return Variable(
            name='flexible carbon emissions profile',
            definition='A time series data points of energy carbon emissions acquired in flexible operation scenario.',
            primitive_type=DefaultPrimitiveType.carbon_emission,
            value_type=ValueType.SERIAL,
            operation_condition=OperationCondition.FLEXIBLE,
        )
    
    @property
    def flexible_carbon_intensity_profile(cls) -> Variable:
        return Variable(
            name='flexible carbon intensity profile',
            definition='A time series data points of energy carbon intensity acquired in flexible operation scenario.',
            primitive_type=DefaultPrimitiveType.carbon_emission_factor,
            value_type=ValueType.SERIAL,
            operation_condition=OperationCondition.FLEXIBLE,
        )
    
    @property
    def flexible_self_production_profile(cls) -> Variable:
        return Variable(
            name='flexible self production profile',
            definition='A time series data points of self-produced acquired in flexible operation scenario.',
            primitive_type=DefaultPrimitiveType.power_demand,
            value_type=ValueType.SERIAL,
            operation_condition=OperationCondition.FLEXIBLE,
        )
    
    @property
    def generic_electric_power_profile(cls) -> Variable:
        return Variable(
            name='generic electric power profile',
            definition='A time series data points of electric power demand acquired in unspecified operation scenario.',
            primitive_type=DefaultPrimitiveType.power_demand,
            value_type=ValueType.SERIAL,
        )

    @property
    def generic_electricity_consumption_profile(cls) -> Variable:
        return Variable(
            name='generic electricity consumption profile',
            definition='A time series data points of electricity consumption acquired in unspecified operation scenario.',
            primitive_type=DefaultPrimitiveType.energy_consumption,
            value_type=ValueType.SERIAL,
        )
    
    @property
    def generic_natural_gas_consumption_profile(cls) -> Variable:
        return Variable(
            name='generic natural gas consumption profile',
            definition='A time series data points of natural gas consumption acquired in unspecified operation scenario.',
            primitive_type=DefaultPrimitiveType.energy_consumption,
            value_type=ValueType.SERIAL,
        )
    
    @property
    def generic_cost_profile(cls) -> Variable:
        return Variable(
            name='generic cost profile',
            definition='A time series data points of energy cost acquired in generic operation scenario.',
            primitive_type=DefaultPrimitiveType.operation_cost,
            value_type=ValueType.SERIAL,
            operation_condition=OperationCondition.GENERIC,
        )
    
    @property
    def generic_carbon_emissions_profile(cls) -> Variable:
        return Variable(
            name='generic carbon emissions profile',
            definition='A time series data points of energy carbon emissions acquired in generic operation scenario.',
            primitive_type=DefaultPrimitiveType.carbon_emission,
            value_type=ValueType.SERIAL,
            operation_condition=OperationCondition.GENERIC,
        )
    
    @property
    def generic_carbon_intensity_profile(cls) -> Variable:
        return Variable(
            name='generic carbon intensity profile',
            definition='A time series data points of energy carbon intensity acquired in generic operation scenario.',
            primitive_type=DefaultPrimitiveType.carbon_emission_factor,
            value_type=ValueType.SERIAL,
            operation_condition=OperationCondition.GENERIC,
        )
    
    @property
    def generic_self_production_profile(cls) -> Variable:
        return Variable(
            name='generic self production profile',
            definition='A time series data points of self-produced acquired in generic operation scenario.',
            primitive_type=DefaultPrimitiveType.power_demand,
            value_type=ValueType.SERIAL,
            operation_condition=OperationCondition.GENERIC,
        )
    
    @property
    def timestamps(cls) -> DateTimeVariable:
        return DateTimeVariable(
            name='timestamps',
            definition='Profile timestamps.',
            primitive_type=DefaultPrimitiveType.timestamp,
            value_type=ValueType.SERIAL,
        )
    
    @property
    def evaluation_start_timestamp(cls) -> DateTimeVariable:
        return DateTimeVariable(
            name='evaluation start timestamp',
            definition='The starting timestamp of an user specified evaluation window.',
            primitive_type=DefaultPrimitiveType.timestamp,
            value_type=ValueType.SINGLE,
        )
    
    @property
    def evaluation_end_timestamp(cls) -> DateTimeVariable:
        return DateTimeVariable(
            name='evaluation end timestamp',
            definition='The starting timestamp of an user specified evaluation window.',
            primitive_type=DefaultPrimitiveType.timestamp,
            value_type=ValueType.SINGLE,
        )
    
    @property
    def load_profile_peak_timestamp(cls) -> DateTimeVariable:
        return DateTimeVariable(
            name='load profile peak timestamp',
            definition='The timestamp of the maximum value of a given load profile.',
            primitive_type=DefaultPrimitiveType.timestamp,
            value_type=ValueType.SINGLE
        )
    
    @property
    def load_profile_valley_timestamp(cls) -> DateTimeVariable:
        return DateTimeVariable(
            name='load profile valley timestamp',
            definition='The timestamp of the minimum value of a given load profile.',
            primitive_type=DefaultPrimitiveType.timestamp,
            value_type=ValueType.SINGLE
        )
    
    @property
    def grid_peak_timestamp(cls) -> DateTimeVariable:
        return DateTimeVariable(
            name='grid peak timestamp',
            definition='The timestamp of the maximum load of the connected grid.',
            primitive_type=DefaultPrimitiveType.timestamp,
            value_type=ValueType.SINGLE
        )
    
    @property
    def generic_signal_start_timestamp(cls) -> DateTimeVariable:
        return DateTimeVariable(
            name='generic_signal_start_timestamp',
            definition='The starting timestamp of a signal e.g. price, emissions, e.t.c.',
            primitive_type=DefaultPrimitiveType.timestamp,
            value_type=ValueType.SINGLE
        )
    
    @property
    def generic_signal_end_timestamp(cls) -> DateTimeVariable:
        return DateTimeVariable(
            name='generic_signal_end_timestamp',
            definition='The ending timestamp of a signal e.g. price, emissions, e.t.c..',
            primitive_type=DefaultPrimitiveType.timestamp,
            value_type=ValueType.SINGLE
        )
    
    @property
    def low_generic_signal_start_timestamp(cls) -> DateTimeVariable:
        return DateTimeVariable(
            name='low_generic_signal_start_timestamp',
            definition='The starting timestamp of a period when a signal e.g. price, emissions, e.t.c. is low.',
            primitive_type=DefaultPrimitiveType.timestamp,
            value_type=ValueType.SINGLE
        )
    
    @property
    def low_generic_signal_end_timestamp(cls) -> DateTimeVariable:
        return DateTimeVariable(
            name='low_generic_signal_end_timestamp',
            definition='The ending timestamp of a period when a signal e.g. price, emissions, e.t.c. is low.',
            primitive_type=DefaultPrimitiveType.timestamp,
            value_type=ValueType.SINGLE
        )
    
    @property
    def medium_generic_signal_start_timestamp(cls) -> DateTimeVariable:
        return DateTimeVariable(
            name='medium_generic_signal_start_timestamp',
            definition='The starting timestamp of a period when a signal e.g. price, emissions, e.t.c. is medium.',
            primitive_type=DefaultPrimitiveType.timestamp,
            value_type=ValueType.SINGLE
        )
    
    @property
    def medium_generic_signal_end_timestamp(cls) -> DateTimeVariable:
        return DateTimeVariable(
            name='medium_generic_signal_end_timestamp',
            definition='The ending timestamp of a period when a signal e.g. price, emissions, e.t.c. is medium.',
            primitive_type=DefaultPrimitiveType.timestamp,
            value_type=ValueType.SINGLE
        )
    
    @property
    def high_generic_signal_start_timestamp(cls) -> DateTimeVariable:
        return DateTimeVariable(
            name='high_generic_signal_start_timestamp',
            definition='The starting timestamp of a period when a signal e.g. price, emissions, e.t.c. is high.',
            primitive_type=DefaultPrimitiveType.timestamp,
            value_type=ValueType.SINGLE
        )
    
    @property
    def high_generic_signal_end_timestamp(cls) -> DateTimeVariable:
        return DateTimeVariable(
            name='high_generic_signal_end_timestamp',
            definition='The ending timestamp of a period when a signal e.g. price, emissions, e.t.c. is high.',
            primitive_type=DefaultPrimitiveType.timestamp,
            value_type=ValueType.SINGLE
        )
    
    @property
    def high_price_start_timestamp(cls) -> DateTimeVariable:
        return DateTimeVariable(
            name='high price start timestamp',
            definition='The starting timestamp of a period when the grid price is high.',
            primitive_type=DefaultPrimitiveType.timestamp,
            value_type=ValueType.SINGLE
        )
    
    @property
    def high_price_end_timestamp(cls) -> DateTimeVariable:
        return DateTimeVariable(
            name='high price end timestamp',
            definition='The ending timestamp of a period when the grid price is high.',
            primitive_type=DefaultPrimitiveType.timestamp,
            value_type=ValueType.SINGLE
        )
    
    @property
    def high_emission_start_timestamp(cls) -> DateTimeVariable:
        return DateTimeVariable(
            name='high emission start timestamp',
            definition='The starting timestamp of a period when the grid emission factor is high.',
            primitive_type=DefaultPrimitiveType.timestamp,
            value_type=ValueType.SINGLE
        )
    
    @property
    def high_emission_end_timestamp(cls) -> DateTimeVariable:
        return DateTimeVariable(
            name='high emission end timestamp',
            definition='The ending timestamp of a period when the grid emission factor is high.',
            primitive_type=DefaultPrimitiveType.timestamp,
            value_type=ValueType.SINGLE
        )
    
    @property
    def floor_area(cls) -> Variable:
        return Variable(
            name='floor area',
            definition='Floor area.',
            primitive_type=DefaultPrimitiveType.area,
            value_type=ValueType.SINGLE,
        )
    
    @property
    def num_zones(cls) -> Variable:
        return Variable(
            name='num_zones',
            definition='num_zones.',
            primitive_type=DefaultPrimitiveType.unspecified,
            value_type=ValueType.SINGLE,
        )
    
    @property
    def num_days(cls) -> Variable:
        return Variable(
            name='num_days',
            definition='num_days.',
            primitive_type=DefaultPrimitiveType.unspecified,
            value_type=ValueType.SINGLE,
        )
    
class DefaultVariable(metaclass=DefaultVariableMetaClass):
    pass

class VariableSet(Definition):
    def __init__(
            self,
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
            floor_area: Union[int,str] = None,
            num_zones: Union[int,str] = None,
            num_days: Union[int,str] = None,
            zone_temperature_profile: List[float] = None,
            cooling_setpoints: List[float] = None,
            heating_setpoints: List[float] = None,
        ) -> None:

        # variables
        self.availability = self.__set_variable(DefaultVariable.availability, availability)
        self.baseline_electric_power_profile = self.__set_variable(DefaultVariable.baseline_electric_power_profile, baseline_electric_power_profile)
        self.baseline_electricity_consumption_profile = self.__set_variable(DefaultVariable.baseline_electricity_consumption_profile, baseline_electricity_consumption_profile)
        self.baseline_natural_gas_consumption_profile = self.__set_variable(DefaultVariable.baseline_natural_gas_consumption_profile, baseline_natural_gas_consumption_profile)
        self.baseline_cost_profile = self.__set_variable(DefaultVariable.baseline_cost_profile, baseline_cost_profile)
        self.baseline_carbon_emissions_profile = self.__set_variable(DefaultVariable.baseline_carbon_emissions_profile, baseline_carbon_emissions_profile)
        self.baseline_carbon_intensity_profile = self.__set_variable(DefaultVariable.baseline_carbon_intensity_profile, baseline_carbon_intensity_profile)
        self.baseline_self_production_profile = self.__set_variable(DefaultVariable.baseline_self_production_profile, baseline_self_production_profile)
        self.flexible_electric_power_profile = self.__set_variable(DefaultVariable.flexible_electric_power_profile, flexible_electric_power_profile)
        self.flexible_electricity_consumption_profile = self.__set_variable(DefaultVariable.flexible_electricity_consumption_profile, flexible_electricity_consumption_profile)
        self.flexible_natural_gas_consumption_profile = self.__set_variable(DefaultVariable.flexible_natural_gas_consumption_profile, flexible_natural_gas_consumption_profile)
        self.flexible_cost_profile = self.__set_variable(DefaultVariable.flexible_cost_profile, flexible_cost_profile)
        self.flexible_carbon_emissions_profile = self.__set_variable(DefaultVariable.flexible_carbon_emissions_profile, flexible_carbon_emissions_profile)
        self.flexible_carbon_intensity_profile = self.__set_variable(DefaultVariable.flexible_carbon_intensity_profile, flexible_carbon_intensity_profile)
        self.flexible_self_production_profile = self.__set_variable(DefaultVariable.flexible_self_production_profile, flexible_self_production_profile)
        self.generic_electric_power_profile = self.__set_variable(DefaultVariable.generic_electric_power_profile, generic_electric_power_profile)
        self.generic_electricity_consumption_profile = self.__set_variable(DefaultVariable.generic_electricity_consumption_profile, generic_electricity_consumption_profile)
        self.generic_natural_gas_consumption_profile = self.__set_variable(DefaultVariable.generic_natural_gas_consumption_profile, generic_natural_gas_consumption_profile)
        self.generic_cost_profile = self.__set_variable(DefaultVariable.generic_cost_profile, generic_cost_profile)
        self.generic_carbon_emissions_profile = self.__set_variable(DefaultVariable.generic_carbon_emissions_profile, generic_carbon_emissions_profile)
        self.generic_carbon_intensity_profile = self.__set_variable(DefaultVariable.generic_carbon_intensity_profile, generic_carbon_intensity_profile)
        self.generic_self_production_profile = self.__set_variable(DefaultVariable.generic_self_production_profile, generic_self_production_profile)
        self.timestamps: DateTimeVariable = self.__set_variable(DefaultVariable.timestamps, timestamps)
        self.evaluation_start_timestamp = self.__set_variable(DefaultVariable.evaluation_start_timestamp, evaluation_start_timestamp)
        self.evaluation_end_timestamp = self.__set_variable(DefaultVariable.evaluation_end_timestamp, evaluation_end_timestamp)
        self.load_profile_peak_timestamp = self.__set_variable(DefaultVariable.load_profile_peak_timestamp, load_profile_peak_timestamp)
        self.load_profile_valley_timestamp = self.__set_variable(DefaultVariable.load_profile_valley_timestamp, load_profile_valley_timestamp)
        self.grid_peak_timestamp = self.__set_variable(DefaultVariable.grid_peak_timestamp, grid_peak_timestamp)
        self.generic_signal_start_timestamp = self.__set_variable(DefaultVariable.generic_signal_start_timestamp, generic_signal_start_timestamp)
        self.generic_signal_end_timestamp = self.__set_variable(DefaultVariable.generic_signal_end_timestamp, generic_signal_end_timestamp)
        self.low_generic_signal_start_timestamp = self.__set_variable(DefaultVariable.low_generic_signal_start_timestamp, low_generic_signal_start_timestamp)
        self.low_generic_signal_end_timestamp = self.__set_variable(DefaultVariable.low_generic_signal_end_timestamp, low_generic_signal_end_timestamp)
        self.medium_generic_signal_start_timestamp = self.__set_variable(DefaultVariable.medium_generic_signal_start_timestamp, medium_generic_signal_start_timestamp)
        self.medium_generic_signal_end_timestamp = self.__set_variable(DefaultVariable.medium_generic_signal_end_timestamp, medium_generic_signal_end_timestamp)
        self.high_generic_signal_start_timestamp = self.__set_variable(DefaultVariable.high_generic_signal_start_timestamp, high_generic_signal_start_timestamp)
        self.high_generic_signal_end_timestamp = self.__set_variable(DefaultVariable.high_generic_signal_end_timestamp, high_generic_signal_end_timestamp)
        self.high_price_start_timestamp = self.__set_variable(DefaultVariable.high_price_start_timestamp, high_price_start_timestamp)
        self.high_price_end_timestamp = self.__set_variable(DefaultVariable.high_price_end_timestamp, high_price_end_timestamp)
        self.high_emission_start_timestamp = self.__set_variable(DefaultVariable.high_emission_start_timestamp, high_emission_start_timestamp)
        self.high_emission_end_timestamp = self.__set_variable(DefaultVariable.high_emission_end_timestamp, high_emission_end_timestamp)
        self.floor_area = self.__set_variable(DefaultVariable.floor_area, floor_area)
        self.num_zones = self.__set_variable(DefaultVariable.num_zones, num_zones)
        self.num_days = self.__set_variable(DefaultVariable.num_days, num_days)
        self.zone_temperature_profile = self.__set_variable(DefaultVariable.zone_temperature_profile, zone_temperature_profile)
        self.cooling_setpoints = self.__set_variable(DefaultVariable.cooling_setpoints, cooling_setpoints)
        self.heating_setpoints = self.__set_variable(DefaultVariable.heating_setpoints, heating_setpoints)
        self.validate_serial_variables()
    
    @property
    def evaluation_length(self) -> int:
        return self.evaluation_mask[self.evaluation_mask].shape[0]
    
    @property
    def evaluation_mask(self) -> np.ndarray:
        # use timesteps for masking and assume evaluation start timestamp and timestep 
        # are integers that indicate timestep
        timestamps = np.array(range(self.__serial_variable_length), dtype=int)\
            if self.timestamps.value is None else self.timestamps.value
        evaluation_start_timestamp = timestamps[0] if self.evaluation_start_timestamp.value is None\
            else self.evaluation_start_timestamp.value
        evaluation_end_timestamp = timestamps[-1] if self.evaluation_end_timestamp.value is None\
            else self.evaluation_end_timestamp.value

        return (timestamps >= evaluation_start_timestamp) & (timestamps <= evaluation_end_timestamp)
    
    def get_temporal_resolution(self, unit: BaseUnit, value: List[datetime.datetime] = None):
        return self.timestamps.get_resolution(unit, value=value)
    
    def validate_serial_variables(self):
        # check that serial variables are of equal length
        variable_lengths = {}

        for _, v in vars(self).items():
            if self.__not_null_serial_variable(v):
                variable_lengths[v.name] = len(v.value)

            else:
                continue
        
        min_length = min(list(variable_lengths.values()))
        max_length = max(list(variable_lengths.values()))
        assert min_length == max_length, f'Unequal serial variable lenghts: {variable_lengths}'
        self.__serial_variable_length = min_length
        
    def __not_null_serial_variable(self, variable: Variable) -> bool:
        return isinstance(variable, Variable)\
            and  variable.value_type == ValueType.SERIAL\
                and isinstance(variable.value, np.ndarray)
    
    def __set_variable(self, default: Variable, value: Any) -> Variable:
        variable = default
        variable.value = value
        
        return variable