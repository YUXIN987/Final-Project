from typing import List, Optional
from statistics import mean
from .houses import House

class HousingMarket:
    def __init__(self, houses: List[House]):
        self.houses: List[House] = houses

    def get_house_by_id(self, house_id: int) -> Optional[House]:
        """
        Retrieve a specific house by ID.
        """
        for house in self.houses:
            if house.id == house_id:
                return house
        return None  # Return None if no house matches the ID

    def calculate_average_price(self, bedrooms: Optional[int] = None) -> float:
        """
        Calculate average house price, optionally filtered by bedrooms.
        """
        if bedrooms is not None:
            houses_filtered = [house for house in self.houses if house.bedrooms == bedrooms and house.available]
        else:
            houses_filtered = [house for house in self.houses if house.available]

        if not houses_filtered:
            return 0.0  # Return 0 if no houses meet the criteria

        return round(mean(house.price for house in houses_filtered), 2)

    def get_houses_that_meet_requirements(self, max_price: int, min_bedrooms: int) -> List[House]:
        """
        Filter houses based on buyer requirements such as maximum price and minimum number of bedrooms.
        """
        filtered_houses = [house for house in self.houses if house.price <= max_price and house.bedrooms >= min_bedrooms and house.available]
        return filtered_houses if filtered_houses else None
