from typing import List
from energy_flexibility_kpis.base import Definition
from energy_flexibility_kpis.enumerations import BaseUnit

class Unit(Definition):
    def __init__(self, numerator: List[BaseUnit] = None, denominator: List[BaseUnit] = None):
        super().__init__()
        self.numerator = numerator
        self.denominator = denominator

    @property
    def numerator(self) -> List[BaseUnit]:
        return self.__numerator
    
    @property
    def denominator(self) -> List[BaseUnit]:
        return self.__denominator
    
    @numerator.setter
    def numerator(self, value: List[BaseUnit]):
        value = [BaseUnit.DIMENSIONLESS] if value is None else value
        self.__numerator = value

    @denominator.setter
    def denominator(self, value: List[BaseUnit]):
        value = [BaseUnit.DIMENSIONLESS] if value is None else value
        self.__denominator = value

    def __str__(self) -> str:
        division_sign = '/'

        if len(self.numerator) == 1:
            if self.numerator[0] == BaseUnit.DIMENSIONLESS:
                if len(self.denominator) > 1 or self.denominator[0] != BaseUnit.DIMENSIONLESS:
                    numerator = '1'
                
                else:
                    numerator = ''
            
            else:
                numerator = self.numerator[0].value[0]
        
        else:
            numerator =  '(' + '*'.join([n.value[0] for n in self.numerator]) + ')'

        if len(self.denominator) == 1:
            if self.denominator[0] == BaseUnit.DIMENSIONLESS:
                division_sign = ''
                denominator = ''
            else:
                denominator = self.denominator[0].value[0]
            
        else:
            denominator =  '(' + '*'.join([d.value[0] for d in self.denominator]) + ')'

        unit = numerator + division_sign + denominator

        return unit
                
        