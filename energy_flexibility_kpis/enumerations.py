from datetime import datetime
from enum import Enum, IntEnum, unique

@unique
class BaseUnit(Enum):
    DIMENSIONLESS = ('', '')
    PERCENT = ('%', 'percent')
    KWH = ('kWh', 'kilowatt-hour')
    KW = ('kW', 'kilowatt')
    DOLLAR = ('%', 'dollar')
    HOUR = ('h', 'hour')
    MINUTE = ('min', 'minute')
    SECOND = ('s', 'second')
    MILLISECOND = ('ms', 'millisecond')
    TON = ('ton', 'ton')
    CELCIUS = ('C', 'celcius')
    KELVIN = ('K', 'kelvin')
    SQUARE_METER = ('m^2', 'square-meter')
    KG_OF_CO2 = ('kgCO2', 'kilograms-of-CO2')
    PPM = ('ppm', 'parts-per-million')

@unique
class ValueType(Enum):
    SERIAL = (list,)
    SINGLE = (str, int, float, bool, datetime)

@unique
class OperationCondition(Enum):
    GENERIC = 'generic'
    BASELINE = 'baseline'
    FLEXIBLE = 'flexible'

@unique
class BaseKPICategory(Enum):
    EF_KPI = 'EF KPI'
    GENERIC = 'Generic'

@unique
class KPICategory(Enum):
    EF_PEAK_POWER_SHEDDING = (BaseKPICategory.EF_KPI, 'Peak Power Shedding')
    EF_ENERGY_OR_AVERAGE_POWER_LOAD_SHEDDING = (BaseKPICategory.EF_KPI, 'Energy/Average Power Load Shedding')
    EF_PEAK_POWER_OR_ENERGY_REBOUND = (BaseKPICategory.EF_KPI, 'Peak Power/Energy Rebound')
    EF_VALLEY_FILLING = (BaseKPICategory.EF_KPI, 'Valley Filling')
    EF_LOAD_SHIFTING = (BaseKPICategory.EF_KPI, 'Load Shifting')
    EF_DEMAND_PROFILE_RESHAPING = (BaseKPICategory.EF_KPI, 'Demand Profile Reshaping')
    EF_ENERGY_STORAGE_CAPABILITY = (BaseKPICategory.EF_KPI, 'Energy Storage Capability')
    EF_DEMAND_RESPONSE_ENERGY_EFFICIENCY = (BaseKPICategory.EF_KPI, 'Demand Response Energy Efficiency')
    EF_DEMAND_RESPONSE_COSTS_OR_SAVINGS = (BaseKPICategory.EF_KPI, 'Demand Response Costs/Savings')
    EF_DEMAND_RESPONSE_EMISSION_OR_ENVIRONMENTAL_IMPACT = (BaseKPICategory.EF_KPI, 'Demand Response Emission/Environmental Impact')
    EF_GRID_INTERACTION = (BaseKPICategory.EF_KPI, 'Grid Interaction')
    EF_IMPACT_ON_IEQ = (BaseKPICategory.EF_KPI, 'Impact on Indoor Environmental Quality')
    GN_BUILDING_ENERGY_EFFICIENCY = (BaseKPICategory.GENERIC, 'Building Energy Efficiency')
    GN_COST_AND_SAVINGS = (BaseKPICategory.GENERIC, 'Cost and Savings')
    GN_CO2_EMISSIONS_OR_ENVIRONMENTAL_IMPACT = (BaseKPICategory.GENERIC, 'CO2 Emissions/Environmental Impact')
    GN_GRID_INTERACTION = (BaseKPICategory.GENERIC, 'Grid Interaction')

@unique
class Relevance(IntEnum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    
@unique
class Stakeholder(Enum):
    DISTRIBUTION_SYSTEM_OPERATOR = 'distribution system operator'
    TRANSMISSION_SYSTEM_OPERATOR = 'transmisssion system operator'
    GRID_OPERATOR = 'grid operator'
    BUILDING_OWNER = 'building owner'
    BUILDING_MANAGER = 'building manager'
    OCCUPANT = 'occupant'
    POWER_SUPPLIER = 'power supplier'
    UTILITY_COMPANY = 'utility company'
    POLICYMAKER = 'policymaker'
    AGGREGATOR = 'aggregator'
    BUILDING_OPERATOR = 'building operator'

@unique
class Complexity(Enum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3

@unique
class TemporalEvaluationWindow(Enum):
    UNSPECIFIED = 'unspecified'
    SINGLE_EVENT = 'single event'
    WHOLE_YEAR = 'whole year'
    WHOLE_DAY = 'whole day'
    MULTIPLE_EVENTS = 'multiple events'

@unique
class TemporalResolution(Enum):
    UNSPECIFIED = 'unspecified'
    HOURLY = 'hourly'
    VARIOUS = 'various'

@unique
class SpatialResolution(Enum):
    UNSPECIFIED = 'unspecified'
    BUILDING_CLUSTER = 'building cluster'
    SINGLE_BUILDING = 'single building'

@unique
class DOEFlexibilityCategory(Enum):
    EFFICIENCY = 'efficiency'
    LOAD_SHIFTING = 'load shifting'
    LOAD_SHEDDING = 'load shedding'
    MODULATING = 'modulating'
    GENERATION = 'generation'

@unique
class PerformanceAspect(Enum):
    POWER = 'power'
    ENERGY = 'energy'
    COST = 'cost'
    EMISSION = 'emission'
    COMFORT = 'comfort'