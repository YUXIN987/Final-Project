from enum import Enum, auto
from dataclasses import dataclass
from typing import Optional
from .houses import House
from .house_market import HousingMarket

class Segment(Enum):
    FANCY = auto()  # Prefers new construction and high quality scores
    OPTIMIZER = auto()  # Looks for best price per square foot value
    AVERAGE = auto()  # Looks for prices below the average market price

@dataclass
class Consumer:
    ID: int
    annual_income: float
    children_number: int
    segment: Segment
    house: Optional[House] = None
    savings: float = 0.0
    saving_rate: float = 0.3
    interest_rate: float = 0.05

    def compute_savings(self, years: int) -> None:
        """
        Calculate accumulated savings over time using the compound interest formula.
        """
        yearly_savings = self.annual_income * self.saving_rate
        for _ in range(years):
            self.savings += yearly_savings
            self.savings *= (1 + self.interest_rate)  # Compound interest

    def buy_a_house(self, housing_market: HousingMarket) -> None:
        """
        Attempt to purchase a suitable house based on consumer preferences and financial capability.
        """
        available_houses = housing_market.houses
        potential_houses = []

        if self.segment == Segment.FANCY:
            potential_houses = [house for house in available_houses if house.is_new_construction() and house.quality_score == QualityScore.EXCELLENT]
        elif self.segment == Segment.OPTIMIZER:
            average_price_per_sqft = housing_market.calculate_average_price_per_sqft()
            potential_houses = [house for house in available_houses if house.calculate_price_per_square_foot() < average_price_per_sqft]
        elif self.segment == Segment.AVERAGE:
            average_price = housing_market.calculate_average_price()
            potential_houses = [house for house in available_houses if house.price < average_price]

        # Sort potential houses by price to prefer cheaper options
        potential_houses.sort(key=lambda house: house.price)

        # Check if there are houses within budget and fitting family size
        for house in potential_houses:
            if house.bedrooms >= self.children_number + 1 and self.savings >= house.price * 0.2:  # Assuming a 20% down payment
                self.house = house
                self.savings -= house.price * 0.2
                house.sell_house()
                break
