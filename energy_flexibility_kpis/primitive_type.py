from typing import Any, Mapping
from energy_flexibility_kpis.base import Definition
from energy_flexibility_kpis.enumerations import BaseUnit
from energy_flexibility_kpis.unit import Unit

class PrimitiveType(Definition):
    def __init__(self, name: str, definition: str, unit: Unit) -> None:
        super().__init__()
        self.name = name
        self.definition = definition
        self.unit = unit

    def info(self) -> Mapping[str, Any]:
        return {
            'name': self.name,
            'definition': self.definition,
            'unit': str(self.unit)
        }

class DefaultPrimitiveTypeMetaClass(type):
    def __init__(cls, *args, **kwargs) -> None:
        pass

    @property
    def power_demand(cls) -> PrimitiveType:
        """An instantaneous power demand of a entity at a moment."""
        
        return PrimitiveType(
            name='power demand',
            definition='An instantaneous power demand of a entity at a moment.',
            unit=Unit(numerator=[BaseUnit.KW])
        )
    
    @property
    def energy_consumption(cls) -> PrimitiveType:
        """The energy consumption of an entiry during a certain period."""
        
        return PrimitiveType(
            name='energy consumption',
            definition='The energy consumption of an entiry during a certain period.',
            unit=Unit(numerator=[BaseUnit.KWH])
        )
    
    @property
    def operation_cost(cls) -> PrimitiveType:
        """The operational cost of an entiry during a certain period."""
        
        return PrimitiveType(
            name='operation cost',
            definition='The operational cost of an entiry during a certain period.',
            unit=Unit(numerator=[BaseUnit.DOLLAR])
        )
    
    @property
    def energy_price(cls) -> PrimitiveType:
        """The price of energy per unit."""
        
        return PrimitiveType(
            name='energy price',
            definition='The price of energy per unit.',
            unit=Unit(numerator=[BaseUnit.DOLLAR], denominator=[BaseUnit.KWH])
        )
    
    @property
    def carbon_emission(cls) -> PrimitiveType:
        """The carbon emission of an entiry during a certain period."""
        
        return PrimitiveType(
            name='carbon emission',
            definition='The carbon emission of an entiry during a certain period.',
            unit=Unit(numerator=[BaseUnit.TON])
        )
    
    @property
    def carbon_emission_factor(cls) -> PrimitiveType:
        """The carbon emission factor of an entiry during a certain period."""
        
        return PrimitiveType(
            name='carbon emission factor',
            definition='The carbon emission factor of an entiry during a certain period.',
            unit=Unit(numerator=[BaseUnit.TON], denominator=[BaseUnit.KWH])
        )
    
    @property
    def temperature(cls) -> PrimitiveType:
        """The temperature of an entity (either an instantaneous value or average value)."""
        
        return PrimitiveType(
            name='temperature',
            definition='The temperature of an entity (either an instantaneous value or average value).',
            unit=Unit(numerator=[BaseUnit.CELCIUS])
        )
    
    @property
    def timestamp(cls) -> PrimitiveType:
        """The datetime of a moment."""
        
        return PrimitiveType(
            name='timestamp',
            definition='The datetime of a moment.',
            unit=Unit(numerator=[BaseUnit.DIMENSIONLESS])
        )
    
    @property
    def duration(cls) -> PrimitiveType:
        """The time difference between two timestamps."""
        
        return PrimitiveType(
            name='duration',
            definition='The time difference between two timestamps.',
            unit=Unit(numerator=[BaseUnit.SECOND])
        )
    
    @property
    def area(cls) -> PrimitiveType:
        """The floor area of a space (e.g., zone, building)."""
        
        return PrimitiveType(
            name='area',
            definition='The floor area of a space (e.g., zone, building).',
            unit=Unit(numerator=[BaseUnit.SQUARE_METER])
        )
    
    @property
    def occupant_count(cls) -> PrimitiveType:
        """The number of occupants in a space."""
        
        return PrimitiveType(
            name='occupant count',
            definition='The number of occupants in a space.',
            unit=Unit(numerator=[BaseUnit.DIMENSIONLESS])
        )
    
    @property
    def unspecified(cls) -> PrimitiveType:
        """Default primitive type."""
        
        return PrimitiveType(
            name='unspecified',
            definition='Default primitive type.',
            unit=Unit(numerator=[BaseUnit.DIMENSIONLESS])
        )

class DefaultPrimitiveType(metaclass=DefaultPrimitiveTypeMetaClass):
    pass