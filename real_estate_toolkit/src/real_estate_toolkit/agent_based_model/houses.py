from enum import Enum
from dataclasses import dataclass
from typing import Optional

class QualityScore(Enum):
    EXCELLENT = 5
    GOOD = 4
    AVERAGE = 3
    FAIR = 2
    POOR = 1

@dataclass
class House:
    id: int
    price: float
    area: float
    bedrooms: int
    year_built: int
    quality_score: Optional[QualityScore] = None
    available: bool = True

    def calculate_price_per_square_foot(self) -> float:
        """
        Calculate and return the price per square foot.
        """
        if self.area == 0:
            return 0
        return round(self.price / self.area, 2)

    def is_new_construction(self, current_year: int = 2024) -> bool:
        """
        Determine if house is considered new construction (< 5 years old).
        """
        age = current_year - self.year_built
        return age < 5

    def get_quality_score(self) -> str:
        """
        Generate a quality score based on house attributes.
        """
        if self.quality_score:
            return f"Quality Score: {self.quality_score.name}"
        else:
            if self.year_built >= 2010:
                return "Quality Score: EXCELLENT"
            elif self.year_built >= 2000:
                return "Quality Score: GOOD"
            elif self.year_built >= 1990:
                return "Quality Score: AVERAGE"
            elif self.year_built >= 1980:
                return "Quality Score: FAIR"
            else:
                return "Quality Score: POOR"

    def sell_house(self) -> None:
        """
        Mark house as sold.
        """
        self.available = False


