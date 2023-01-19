# import native python modules
import datetime
from typing import List, Union

# import installed python modules
import pandas as pd

# import package modules
from energy_flexibility_kpis.utilities import Parser

def peak_power_reduction(grid_peak_timestamp: Union[str, datetime.datetime], baseline_electric_power_profile: List[float], flexible_electric_power_profile: List[float], timestamps: List[Union[str, datetime.datetime]]) -> float:
    """Reduced power demand during peak hour due to flexible operation.

    Calculates the difference in daily peak between the baseline and flexible profiles.

    Parameters
    ----------
    grid_peak_timestamp: Union[str, datetime.datetime]
        Demand response signal occurence timestamp, [YYYY-mm-dd HH:MM:SS].
    baseline_electric_power_profile : List[float]
        Electric power profile for baseline scenario during evaluation period, [kW].
    flexible_electric_power_profile : List[float]
        Electric power profile for flexible scenario during evaluation period, [kW].
    timestamps : List[Union[str, datetime.datetime]]
        Evaluation period timestamps, [YYYY-mm-dd HH:MM:SS].

    Returns
    -------
    peak_power_reduction : float
        Reduced power demand, [kW].
    """

    df = pd.DataFrame({
        'timestamp': timestamps,
        'baseline_electric_power': baseline_electric_power_profile,
        'flexible_electric_power': flexible_electric_power_profile
    })
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df['peak_power_reduction'] = df['baseline_electric_power'] - df['flexible_electric_power']
    peak_power_reduction = df[df['timestamp'] == grid_peak_timestamp]['peak_power_reduction'].iloc[0]

    return peak_power_reduction

def flexibility_factor(generic_electricity_consumption_profile: List[float], high_price_start_timestamp: Union[str, datetime.datetime], high_price_end_timestamp: Union[str, datetime.datetime], timestamps: List[Union[str, datetime.datetime]]) -> float:
    """Ability to shift a quantity (e.g., energy, cost, emissions) from high-load periods to low-load periods. It ranges between -1 (quantity was only during high-load periods) and 1 (quantity was only during low-load periods).

    Calculates the ratio of the difference between electricity consumption during high-price period and low-price period, and sum of electricity consumption during high-price period and low-price period.

    Parameters
    ----------
    generic_electricity_consumption_profile : List[float]
        Electricity consumption profile during evaluation period, [kWh].
    high_price_start_timestamp : Union[str, datetime.datetime]
        Peak price start timestamp, [YYYY-mm-HH:MM:SS].
    high_price_end_timestamp : Union[str, datetime.datetime]
        Peak price end timestamp, [YYYY-mm-HH:MM:SS].
    timestamps : List[Union[str, datetime.datetime]]
        Evaluation period timestamps, [YYYY-mm-dd HH:MM:SS].

    Returns
    -------
    flexibility_factor : float
        Flexibility factor, [-].
    """

    df = pd.DataFrame({
        'timestamp': timestamps,
        'generic_electricity_consumption': generic_electricity_consumption_profile
    })
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    high_price_electricity_consumption = df[
        (df['timestamp'] >= high_price_start_timestamp) & (df['timestamp'] <= high_price_end_timestamp)
    ]['generic_electricity_consumption'].sum()
    low_price_electricity_consumption = df[
        (df['timestamp'] < high_price_start_timestamp) & (df['timestamp'] > high_price_end_timestamp)
    ]['generic_electricity_consumption'].sum()
    flexibility_factor = (low_price_electricity_consumption - high_price_electricity_consumption)/\
        (low_price_electricity_consumption + high_price_electricity_consumption)

    return flexibility_factor
    

def load_factor(generic_electric_power_profile: List[float], load_profile_peak_timestamp: Union[str, datetime.datetime], timestamps: List[Union[str, datetime.datetime]]) -> float:
    """Ratio of the average load to the peak load during an evaluation period.

    Parameters
    ----------
    generic_electric_power_profile : List[float]
        Electricity power profile during evaluation period, [kW].
    load_profile_peak_timestamp : Union[str, datetime.datetime]
        Peak power timestamp, [YYYY-mm-HH:MM:SS].
    timestamps : List[Union[str, datetime.datetime]]
        Evaluation period timestamps, [YYYY-mm-dd HH:MM:SS].

    Returns
    -------
    load_factor : float
        Load factor, [-].
    """

    df = pd.DataFrame({
        'timestamp': timestamps,
        'generic_electric_power': generic_electric_power_profile
    })
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    load_factor = df['generic_electric_power'].mean()/df[df['timestamp'] == load_profile_peak_timestamp]['generic_electric_power'].iloc[0]

    return load_factor

def building_energy_flexibility_index(baseline_electric_power_profile: List[float], flexible_electric_power_profile: List[float]):
    """The average power reduction/increase.
    
    Calculates the difference between the energy used by a baseline (reference) load profile scenario and the energy used in a new, flexible event scenario divided by the duration of the event.

    Parameters
    ----------
    baseline_electric_power_profile : List[float]
        Electric power profile for baseline scenario during evaluation period, [kW].
    flexible_electric_power_profile : List[float]
        Electric power profile for flexible scenario during evaluation period, [kW].

    Returns
    -------
    building_energy_flexibility_index : float
        Building energy flexibility index, [kW].
    """

    building_energy_flexibility_index = (
        sum(baseline_electric_power_profile) - sum(flexible_electric_power_profile)
    )/len(baseline_electric_power_profile)

    return building_energy_flexibility_index