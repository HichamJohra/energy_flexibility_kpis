# import native python modules
from datetime import datetime
from typing import List, Union

# import installed python modules
import pandas as pd

# import package modules
pass

def peak_power_shedding(timestamps: List[Union[str, datetime]], baseline_power: List[float], flexible_power: List[float]) -> List[float]:
    r"""Reduced power demand during peak hour due to flexible operation.

    Calculates the difference in daily peak between the baseline and flexible profiles.

    Parameters
    ----------
    timestamps : List[Union[str, datetime]]
        Time series timestamps, [YYYY-mm-dd HH:SS:MM].
    baseline_power : List[float]
        Peak power demand of baseline scenario, [W].
    flexible_power : List[float]
        Peak power demand of flexible scenario, [W].

    Returns
    -------
    peak_power_shedding : List[float]
        Reduced power demand, [W].
    """

    df = pd.DataFrame({
        'timestamp': timestamps,
        'baseline_power': baseline_power,
        'flexible_power': flexible_power
    })
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df['date'] = df['timestamp'].dt.normalize()
    df = df.groupby([df['timestamp'].dt.date]).max()
    peak_power_shedding = (df['baseline_power'] - df['flexible_power']).tolist()

    return peak_power_shedding