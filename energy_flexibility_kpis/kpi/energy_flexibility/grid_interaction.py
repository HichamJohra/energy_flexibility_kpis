import datetime
from typing import List, Union
from energy_flexibility_kpis.kpi.base import KPI

class SelfConsumptionDuringDRAction(KPI):
    """The proportion of increased demand covered by onsite generation. This indicator 
    is a measure of the coincidence between locally produced electricity and increased 
    demand during a DR action."""

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
        
        raise NotImplementedError
    
class RelativeEnergyImportSavings(KPI):
    """Energy import savings (reduction of the residual power demand that is not covered 
    by local RES production) during demand response period in comparison to the reference 
    operation."""

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
        
        raise NotImplementedError
    
class FlexibilityAggregationSynergyFactor(KPI):
    """Quantify the benefit of aggregating multiple flexible systems by measuring the 
    amount of additional Secondary Frequency Regulation (SFR) capacity that is available 
    from the aggregation relative to the sum of SFR capacities the systems could 
    provide individually."""

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
        
        raise NotImplementedError