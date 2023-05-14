import datetime
from typing import List, Union
import numpy as np
import pandas as pd
from energy_flexibility_kpis.variable import DefaultVariable, Variable
from energy_flexibility_kpis.enumerations import KPICategory, ValueType

class KPI:
    def __init__(self, category: KPICategory) -> None:
        self.category = category
        self.__kpi = np.nan
        self.baseline_electric_power = DefaultVariable.BASELINE_ELECTRIC_POWER.value.copy()
        self.baseline_electricity_consumption_profile = DefaultVariable.BASELINE_ELECTRICITY_CONSUMPTION_PROFILE.value.copy()
        self.baseline_natural_gas_consumption_profile = DefaultVariable.BASELINE_NATURAL_GAS_CONSUMPTION_PROFILE.value.copy()
        self.flexible_electric_power = DefaultVariable.FLEXIBLE_ELECTRIC_POWER.value.copy()
        self.flexible_electricity_consumption_profile = DefaultVariable.FLEXIBLE_ELECTRICITY_CONSUMPTION_PROFILE.value.copy()
        self.flexible_natural_gas_consumption_profile = DefaultVariable.FLEXIBLE_NATURAL_GAS_CONSUMPTION_PROFILE.value.copy()
        self.generic_electric_power = DefaultVariable.GENERIC_ELECTRIC_POWER.value.copy()
        self.generic_electricity_consumption_profile = DefaultVariable.GENERIC_ELECTRICITY_CONSUMPTION_PROFILE.value.copy()
        self.generic_natural_gas_consumption_profile = DefaultVariable.GENERIC_NATURAL_GAS_CONSUMPTION_PROFILE.value.copy()
        self.timestamps = DefaultVariable.TIMESTAMPS.value.copy()
        self.evaluation_start_timestamp = DefaultVariable.EVALUATION_START_TIMESTAMP.value.copy()
        self.evaluation_end_timestamp = DefaultVariable.EVALUATION_END_TIMESTAMP.value.copy()

    @property
    def kpi(self) -> Union[float, List[float]]:
        return self.__kpi
    
    @kpi.setter
    def kpi(self, value: Union[float, List[float]]):
        # reset variable values to None save memory
        for v in vars(self):
            if isinstance(v, Variable):
                v.value = None
            else:
                continue

        self.__kpi = value

    def update_variables(self, **kwargs) -> pd.DataFrame:    
        for k, v in kwargs.items():
            try:
                vars(self)[k].value = v

            except KeyError:
                continue

        self.__validate_serial_variables()

        # set serial variables to evaluation window if evaluation
        # timestamps are provided
        # for v in vars(self):
        #     if self.__not_null_serial_variable(v):
        #         v.value = v.value[]


    def __validate_serial_variables(self):
        # check that serial variables are of equal length
        variable_lengths = {}

        for v in vars(self):
            if self.__not_null_serial_variable(v):
                variable_lengths[v.name] = len(v.value)
            else:
                continue

        assert min(list(variable_lengths.values())) == max(list(variable_lengths.values())),\
            f'Unequal serial variable lenghts: {variable_lengths}'
        
    def __not_null_serial_variable(self, variable: Variable):
        return isinstance(variable, Variable)\
            and  variable.value_type == ValueType.SERIAL\
                and isinstance(variable.value, np.ndarray)

    def calculate(self, **kwargs) -> Union[float, List[float]]:
        self.kpi = None
        self.update_variables(**kwargs)
        
        return np.nan

class BuildingEnergyFlexibilityKPI(KPI):
    def __init__(self):
        """The average power reduction/increase.
        
        Calculates the difference between the energy used by a baseline (reference) load profile scenario and the energy used in a new, flexible event scenario divided by the duration of the event.
        """

        super().__init__(category=KPICategory.ENERGY_OR_AVERAGE_POWER_LOAD_SHEDDING)

    def calculate(
        self, timestamps: List[Union[str, datetime.datetime]], baseline_electric_power_profile: List[float], flexible_electric_power_profile: List[float], 
        evaluation_start_timestamp: Union[str, datetime.datetime] = None, evaluation_end_timestamp: Union[str, datetime.datetime] = None
    ) -> float:
        """Calculate building energy flexibility KPI

        Parameters
        ----------
        timestamps : List[Union[str, datetime.datetime]]
            Profile timestamps, [YYYY-mm-dd HH:MM:SS].
        baseline_electric_power_profile : List[float]
            Electric power profile for baseline scenario during evaluation period, [kW].
        flexible_electric_power_profile : List[float]
            Electric power profile for flexible scenario during evaluation period, [kW].
        evaluation_start_timestamp: Union[str, datetime.datetime], optional
            Start of the evaluation window for profiles.
        evaluation_end_timestamp: Union[str, datetime.datetime], optional
            End of the evaluation window for profiles.

        Returns
        -------
        kpi : float
            Building energy flexibility index, [kW].
        """

        _ = super().calculate(
            timestamps=timestamps, 
            baseline_electric_power_profile=baseline_electric_power_profile, 
            flexible_electric_power_profile=flexible_electric_power_profile, 
            evaluation_start_timestamp=evaluation_start_timestamp, 
            evaluation_end_timestamp=evaluation_end_timestamp
        )
        kpi = (self.baseline_electric_power.value.sum() - self.flexible_electric_power.value.sum())/len(self.baseline_electric_power.value)
        self.kpi = kpi

        return self.kpi