import datetime
from typing import Union

class Parser:
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

        return time if isinstance(time, datetime.time) else Parser.string_to_time(time)

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