import re  # Import regular expression library for text manipulation
from dataclasses import dataclass
from typing import Dict, List, Any

@dataclass
class Cleaner:
    """Class for cleaning real estate data."""
    data: List[Dict[str, Any]]

    def rename_with_best_practices(self) -> None:
        """ Rename the columns with best practices """
        if not self.data:
            return
        
        old_new_names = {}
        for key in self.data[0].keys():
            # Convert to snake_case
            new_key = re.sub(r'(?<!^)(?=[A-Z])', '_', key).lower()  # Add underscore before uppercase letters not at the start
            new_key = new_key.replace(' ', '_')  # Replace spaces with underscores
            old_new_names[key] = new_key

        for row in self.data:
            for old_key, new_key in old_new_names.items():
                row[new_key] = row.pop(old_key)

    def na_to_none(self) -> List[Dict[str, Any]]:
        """
        Replace 'NA' with None in all values with 'NA' in the dictionary.
        Returns a new list of dictionaries with the modifications.
        """
        return [{k: (None if v == 'NA' else v) for k, v in row.items()} for row in self.data]

