# import native python modules
import datetime
from typing import List, Union

# import installed python modules
import pandas as pd

# import package modules
from energy_flexibility_kpis.utilities import Preprocess

def peak_power_reduction(
    timestamps: List[Union[str, datetime.datetime]], grid_peak_timestamp: Union[str, datetime.datetime], baseline_electric_power_profile: List[float], 
    flexible_electric_power_profile: List[float], evaluation_start_timestamp: Union[str, datetime.datetime] = None, evaluation_end_timestamp: Union[str, datetime.datetime] = None
) -> float:
    """Reduced power demand during peak hour due to flexible operation.

    Calculates the difference in daily peak between the baseline and flexible profiles at the grid peak timestamp.

    Parameters
    ----------
    timestamps : List[Union[str, datetime.datetime]]
        Profile timestamps, [YYYY-mm-dd HH:MM:SS].
    grid_peak_timestamp: Union[str, datetime.datetime]
        Demand response signal occurence timestamp, [YYYY-mm-dd HH:MM:SS].
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
        Reduced power demand, [kW].
    """

    df = __set_df(
        evaluation_start_timestamp=evaluation_start_timestamp, 
        evaluation_end_timestamp=evaluation_end_timestamp,
        timestamps=timestamps, 
        baseline_electric_power_profile=baseline_electric_power_profile, 
        flexible_electric_power_profile=flexible_electric_power_profile
    )

    df['peak_power_reduction'] = df['baseline_electric_power'] - df['flexible_electric_power']
    kpi = df[df['timestamp'] == grid_peak_timestamp]['peak_power_reduction'].iloc[0]

    return kpi

def flexibility_factor(
    timestamps: List[Union[str, datetime.datetime]], generic_electricity_consumption_profile: List[float], high_price_start_timestamp: Union[str, datetime.datetime], 
    high_price_end_timestamp: Union[str, datetime.datetime], evaluation_start_timestamp: Union[str, datetime.datetime] = None, evaluation_end_timestamp: Union[str, datetime.datetime] = None
) -> float:
    """Ability to shift a quantity (e.g., energy, cost, emissions) from high-load periods to low-load periods. It ranges between -1 (quantity was only during high-load periods) and 1 (quantity was only during low-load periods).

    Calculates the ratio of the difference between electricity consumption during high-price period and low-price period, and sum of electricity consumption during high-price period and low-price period.

    Parameters
    ----------
    timestamps : List[Union[str, datetime.datetime]]
        Profile timestamps, [YYYY-mm-dd HH:MM:SS].
    generic_electricity_consumption_profile : List[float]
        Electricity consumption profile during evaluation period, [kWh].
    high_price_start_timestamp : Union[str, datetime.datetime]
        Peak price start timestamp, [YYYY-mm-HH:MM:SS].
    high_price_end_timestamp : Union[str, datetime.datetime]
        Peak price end timestamp, [YYYY-mm-HH:MM:SS].
    evaluation_start_timestamp: Union[str, datetime.datetime], optional
        Start of the evaluation window for profiles.
    evaluation_end_timestamp: Union[str, datetime.datetime], optional
        End of the evaluation window for profiles.

    Returns
    -------
    kpi : float
        Flexibility factor, [-].
    """

    df = __set_df(
        evaluation_start_timestamp=evaluation_start_timestamp, 
        evaluation_end_timestamp=evaluation_end_timestamp,
        timestamps=timestamps, 
        generic_electricity_consumption_profile=generic_electricity_consumption_profile
    )

    high_price_electricity_consumption = df[
        (df['timestamp'] >= high_price_start_timestamp) & (df['timestamp'] <= high_price_end_timestamp)
    ]['generic_electricity_consumption'].sum()
    low_price_electricity_consumption = df[
        (df['timestamp'] < high_price_start_timestamp) | (df['timestamp'] > high_price_end_timestamp)
    ]['generic_electricity_consumption'].sum()
    kpi = (low_price_electricity_consumption - high_price_electricity_consumption)/\
        (low_price_electricity_consumption + high_price_electricity_consumption)

    return kpi
    
def load_factor(
    timestamps: List[Union[str, datetime.datetime]], generic_electric_power_profile: List[float], load_profile_peak_timestamp: Union[str, datetime.datetime], 
    evaluation_start_timestamp: Union[str, datetime.datetime] = None, evaluation_end_timestamp: Union[str, datetime.datetime] = None
) -> float:
    """Ratio of the average load to the peak load during an evaluation period.

    Parameters
    ----------
    timestamps : List[Union[str, datetime.datetime]]
        Profile timestamps, [YYYY-mm-dd HH:MM:SS].
    generic_electric_power_profile : List[float]
        Electricity power profile during evaluation period, [kW].
    load_profile_peak_timestamp : Union[str, datetime.datetime]
        Peak power timestamp, [YYYY-mm-HH:MM:SS].
    evaluation_start_timestamp: Union[str, datetime.datetime], optional
        Start of the evaluation window for profiles.
    evaluation_end_timestamp: Union[str, datetime.datetime], optional
        End of the evaluation window for profiles.

    Returns
    -------
    kpi : float
        Load factor, [-].
    """

    df = __set_df(
        evaluation_start_timestamp=evaluation_start_timestamp, 
        evaluation_end_timestamp=evaluation_end_timestamp,
        timestamps=timestamps, 
        generic_electric_power_profile=generic_electric_power_profile
    )

    kpi = df['generic_electric_power'].mean()/df[df['timestamp'] == load_profile_peak_timestamp]['generic_electric_power'].iloc[0]

    return kpi

def building_energy_flexibility_index(
    timestamps: List[Union[str, datetime.datetime]], baseline_electric_power_profile: List[float], flexible_electric_power_profile: List[float], 
    evaluation_start_timestamp: Union[str, datetime.datetime] = None, evaluation_end_timestamp: Union[str, datetime.datetime] = None
) -> float:
    """The average power reduction/increase.
    
    Calculates the difference between the energy used by a baseline (reference) load profile scenario and the energy used in a new, flexible event scenario divided by the duration of the event.

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

    df = __set_df(
        evaluation_start_timestamp=evaluation_start_timestamp, 
        evaluation_end_timestamp=evaluation_end_timestamp,
        timestamps=timestamps, 
        baseline_electric_power_profile=baseline_electric_power_profile,
        flexible_electric_power_profile=flexible_electric_power_profile,
    )

    kpi = (
        df['baseline_electric_power'].sum() - df['flexible_electric_power'].sum()
    )/df.shape[0]

    return kpi

def hourly_relative_power_demand_reduction(
    timestamps: List[Union[str, datetime.datetime]], baseline_electric_power_profile: List[float], flexible_electric_power_profile: List[float], 
    evaluation_start_timestamp: Union[str, datetime.datetime] = None, evaluation_end_timestamp: Union[str, datetime.datetime] = None
) -> List[float]:
    df = __set_df(
        evaluation_start_timestamp=evaluation_start_timestamp, 
        evaluation_end_timestamp=evaluation_end_timestamp,
        timestamps=timestamps, 
        baseline_electric_power_profile=baseline_electric_power_profile,
        flexible_electric_power_profile=flexible_electric_power_profile,
    )
    kpi = (df['baseline_electric_power'] - df['flexible_electric_power'])/df['baseline_electric_power']
    kpi = kpi.tolist()

    return kpi

def relative_peak_power_demand_reduction(
    timestamps: List[Union[str, datetime.datetime]], baseline_electric_power_profile: List[float], flexible_electric_power_profile: List[float], 
    evaluation_start_timestamp: Union[str, datetime.datetime] = None, evaluation_end_timestamp: Union[str, datetime.datetime] = None
) -> float:
    df = __set_df(
        evaluation_start_timestamp=evaluation_start_timestamp, 
        evaluation_end_timestamp=evaluation_end_timestamp,
        timestamps=timestamps, 
        baseline_electric_power_profile=baseline_electric_power_profile,
        flexible_electric_power_profile=flexible_electric_power_profile,
    )
    kpi = 1 - (df['flexible_electric_power'].max()/df['baseline_electric_power'].max())
    kpi = kpi.tolist()

    return kpi

def annual_average_daily_load_variation(
    timestamps: List[Union[str, datetime.datetime]], generic_electric_power_profile: List[float],
    evaluation_start_timestamp: Union[str, datetime.datetime] = None, evaluation_end_timestamp: Union[str, datetime.datetime] = None
) -> float:
    # need to put in docs that evaluation period must be within a year
    df = __set_df(
        evaluation_start_timestamp=evaluation_start_timestamp, 
        evaluation_end_timestamp=evaluation_end_timestamp,
        timestamps=timestamps, 
        generic_electric_power_profile=generic_electric_power_profile,
    )
    hourly_average_load = df.groupby(['date', 'hour'])['generic_electric_power'].mean().tolist()
    daily_average_load = df.groupby(['date'])['generic_electric_power'].mean().tolist()
    years = df['year'].unique()
    assert len(years) == 1, f'Evaluation period must be within the same year. The provided data has the following years: {years}'
    
    annual_average_load = df['generic_electric_power'].mean()
    total = 0

    for h in hourly_average_load:
        for d in daily_average_load:
            total += abs(h - d)
    
    kpi = 0.5*total*100.0/(annual_average_load*len(hourly_average_load))

    return kpi

def peak_power_rebound(
    timestamps: List[Union[str, datetime.datetime]], baseline_electric_power_profile: List[float], flexible_electric_power_profile: List[float], 
    evaluation_start_timestamp: Union[str, datetime.datetime] = None, evaluation_end_timestamp: Union[str, datetime.datetime] = None
) -> float:
    df = __set_df(
        evaluation_start_timestamp=evaluation_start_timestamp, 
        evaluation_end_timestamp=evaluation_end_timestamp,
        timestamps=timestamps, 
        baseline_electric_power_profile=baseline_electric_power_profile,
        flexible_electric_power_profile=flexible_electric_power_profile,
    )
    kpi = df['baseline_electric_power'].max() - df['flexible_electric_power'].max()

    return kpi

def average_power_rebound(
    timestamps: List[Union[str, datetime.datetime]], baseline_electric_power_profile: List[float], flexible_electric_power_profile: List[float], 
    evaluation_start_timestamp: Union[str, datetime.datetime] = None, evaluation_end_timestamp: Union[str, datetime.datetime] = None
) -> float:
    df = __set_df(
        evaluation_start_timestamp=evaluation_start_timestamp, 
        evaluation_end_timestamp=evaluation_end_timestamp,
        timestamps=timestamps, 
        baseline_electric_power_profile=baseline_electric_power_profile,
        flexible_electric_power_profile=flexible_electric_power_profile,
    )
    kpi = df['baseline_electric_power'].mean() - df['flexible_electric_power'].mean()

    return kpi

def deviation_decrease_from_the_flat_demand_profile(
    timestamps: List[Union[str, datetime.datetime]], baseline_electric_power_profile: List[float], flexible_electric_power_profile: List[float], 
    evaluation_start_timestamp: Union[str, datetime.datetime] = None, evaluation_end_timestamp: Union[str, datetime.datetime] = None
):
    df = __set_df(
        evaluation_start_timestamp=evaluation_start_timestamp, 
        evaluation_end_timestamp=evaluation_end_timestamp,
        timestamps=timestamps, 
        baseline_electric_power_profile=baseline_electric_power_profile,
        flexible_electric_power_profile=flexible_electric_power_profile,
    )
    kpi = 1 - (df['flexible_electric_power'].var()/df['baseline_electric_power'].var())**0.5

    return kpi

def ramp(
    timestamps: List[Union[str, datetime.datetime]], generic_electric_power_profile: List[float],
    evaluation_start_timestamp: Union[str, datetime.datetime] = None, evaluation_end_timestamp: Union[str, datetime.datetime] = None
) -> List[float]:
    df = __set_df(
        evaluation_start_timestamp=evaluation_start_timestamp, 
        evaluation_end_timestamp=evaluation_end_timestamp,
        timestamps=timestamps, 
        generic_electric_power_profile=generic_electric_power_profile,
    )
    kpi = df['generic_electric_power_profile'] - df['generic_electric_power_profile'].shift(1)
    kpi = kpi.tolist()

    return kpi

def __set_df(
    evaluation_start_timestamp: Union[str, datetime.datetime], evaluation_end_timestamp: Union[str, datetime.datetime], 
    timestamps: List[Union[str, datetime.datetime]], baseline_electric_power_profile: List[float] = None, flexible_electric_power_profile: List[float] = None,
    generic_electricity_consumption_profile: List[float] = None, generic_electric_power_profile: List[float] = None
):
    df = {
        'timestamp': timestamps,
        'baseline_electric_power': baseline_electric_power_profile,
        'flexible_electric_power': flexible_electric_power_profile,
        'generic_electricity_consumption': generic_electricity_consumption_profile,
        'generic_electric_power': generic_electric_power_profile,
    }
    
    # check that all fields that are provided have equal length
    fields = {k: len(v) for k, v in df.items() if v is not None}

    if len(fields) == 0 or 'timestamp' not in fields.keys():
        raise Exception('timestamp field cannot be None. Supply a list of timestamps to the initialization function.')
    elif min(fields.values()) != max(fields.values()):
        raise Exception(f'Unequal profile lengths: {fields}.')
    else:
        pass
    
    data_length = list(fields.values())[0]
    df = {k:v if v is not None else [None]*data_length for k, v in df.items()}
    df = pd.DataFrame(df)

    if evaluation_start_timestamp is not None:
        df = df[df['timestamp'] >= evaluation_start_timestamp]
    else:
        pass

    if evaluation_end_timestamp is not None:
        df = df[df['timestamp'] <= evaluation_end_timestamp]
    else:
        pass

    df = Preprocess.set_timestamp_fields(df)
    
    return df

    