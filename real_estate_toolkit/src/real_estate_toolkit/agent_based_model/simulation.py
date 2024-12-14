from enum import Enum, auto
from dataclasses import dataclass, field
from random import gauss, randint, shuffle, choice
from typing import List, Dict, Any
from .houses import House
from .house_market import HousingMarket
from .consumers import Segment, Consumer

class CleaningMarketMechanism(Enum):
    INCOME_ORDER_DESCENDANT = auto()
    INCOME_ORDER_ASCENDANT = auto()
    RANDOM = auto()

@dataclass
class AnnualIncomeStatistics:
    minimum: float
    average: float
    standard_deviation: float
    maximum: float

@dataclass
class ChildrenRange:
    minimum: int = 0
    maximum: int = 5

@dataclass
class Simulation:
    housing_market_data: List[Dict[str, Any]]
    consumers_number: int
    years: int
    annual_income: AnnualIncomeStatistics
    children_range: ChildrenRange
    cleaning_market_mechanism: CleaningMarketMechanism
    down_payment_percentage: float = 0.2
    saving_rate: float = 0.3
    interest_rate: float = 0.05
    housing_market: HousingMarket = field(init=False)
    consumers: List[Consumer] = field(init=False)

    def create_housing_market(self):
        houses = [House(**data) for data in self.housing_market_data]
        self.housing_market = HousingMarket(houses=houses)

    def create_consumers(self):
        self.consumers = []
        for _ in range(self.consumers_number):
            income = gauss(self.annual_income.average, self.annual_income.standard_deviation)
            while income < self.annual_income.minimum or income > self.annual_income.maximum:
                income = gauss(self.annual_income.average, self.annual_income.standard_deviation)
            children = randint(self.children_range.minimum, self.children_range.maximum)
            segment = choice(list(Segment))
            consumer = Consumer(
                ID=_,
                annual_income=income,
                children_number=children,
                segment=segment,
                savings=0.0,
                saving_rate=self.saving_rate,
                interest_rate=self.interest_rate
            )
            self.consumers.append(consumer)

    def compute_consumers_savings(self):
        for consumer in self.consumers:
            consumer.compute_savings(self.years)

    def clean_the_market(self):
        if self.cleaning_market_mechanism == CleaningMarketMechanism.INCOME_ORDER_DESCENDANT:
            self.consumers.sort(key=lambda x: x.annual_income, reverse=True)
        elif self.cleaning_market_mechanism == CleaningMarketMechanism.INCOME_ORDER_ASCENDANT:
            self.consumers.sort(key=lambda x: x.annual_income)
        elif self.cleaning_market_mechanism == CleaningMarketMechanism.RANDOM:
            shuffle(self.consumers)

        for consumer in self.consumers:
            consumer.buy_a_house(self.housing_market)

    def compute_owners_population_rate(self) -> float:
        owners = sum(1 for consumer in self.consumers if consumer.house is not None)
        return owners / self.consumers_number if self.consumers_number > 0 else 0

    def compute_houses_availability_rate(self) -> float:
        available_houses = sum(1 for house in self.housing_market.houses if house.available)
        total_houses = len(self.housing_market.houses)
        return available_houses / total_houses if total_houses > 0 else 0


