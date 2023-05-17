# import native python modules
import datetime
from typing import Union

# import installed python modules
import pandas as pd

class Preprocess:
    @staticmethod
    def parse_time(time: Union[str, datetime.time]) -> datetime.time:
        r"""Return datetime.time instance if str instance.

        Parameters
        ----------
        time: Union[str, datetime.time]
            Time definition.

        Returns
        -------
        time : datetime.time
            datetime.time instance.
        """

        return time if isinstance(time, datetime.time) else Preprocess.string_to_time(time)

    @staticmethod
    def string_to_time(string: str) -> datetime.time:
        r"""Convert string represention of time to datetime.time instance.

        Parameters
        ----------
        string: str
            Time string, [HH:MM:SS].

        Returns
        -------
        time : datetime.time
            datetime.time instance.
        """

        time = datetime.time(*[int(v) for v in string.split(':')])

        return time

    @staticmethod
    def set_timestamp_fields(df: pd.DataFrame) -> pd.DataFrame:
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df['date'] = df['timestamp'].dt.normalize()
        df['year'] = df['timestamp'].dt.year
        df['month'] = df['timestamp'].dt.month
        df['day_of_month'] = df['timestamp'].dt.day
        df['day_of_week'] = df['timestamp'].dt.day_of_week
        df['hour'] = df['timestamp'].dt.hour
        df['day_of_year'] = df['timestamp'].dt.day_of_year

        return df