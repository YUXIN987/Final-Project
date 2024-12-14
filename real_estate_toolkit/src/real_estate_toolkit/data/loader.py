import pandas as pd
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Any

@dataclass
class DataLoader:
    """Class for loading and basic processing of real estate data."""
    data_path: Path

    def load_data_from_csv(self) -> List[Dict[str, Any]]:
        """Load data from a CSV file into a list of dictionaries."""
        try:
            df = pd.read_csv(self.data_path)
            return df.to_dict(orient='records')
        except Exception as e:
            print(f"Error loading data: {e}")
            return []

    def validate_columns(self, data: List[Dict[str, Any]], required_columns: List[str]) -> bool:
        """ Validate that all required columns are present in the dataset. """
        if not data:
            print("No data loaded. Cannot validate columns.")
            return False
        
        data_columns = set(data[0].keys())  # assuming 'data' is not empty
        missing_columns = [col for col in required_columns if col not in data_columns]
        
        if missing_columns:
            print(f"Missing required columns: {missing_columns}")
            return False
        else:
            print("All required columns are present.")
            return True


    

