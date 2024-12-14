import statistics
from dataclasses import dataclass
from typing import Dict, List, Tuple, Any, Union, Optional
import numpy as np

@dataclass
class Descriptor:
    """Class for summarizing and describing real estate data."""
    data: List[Dict[str, Any]]

    def none_ratio(self, columns: Union[List[str], str] = "all") -> Dict[str, float]:
        """Compute the ratio of None values per column."""
        if columns == "all":
            columns = self.data[0].keys()
        none_ratios = {}
        for column in columns:
            if column not in self.data[0]:
                raise ValueError(f"Column {column} does not exist in the data.")
            total = sum(1 for row in self.data if row.get(column) is None)
            none_ratios[column] = total / len(self.data)
        return none_ratios

    def average(self, columns: Union[List[str], str] = "all"):
        """Compute the average value for numeric variables, omit None values."""
        if columns == "all":
            columns = [col for col in self.data[0].keys() if isinstance(self.data[0][col], (int, float, type(None)))]
        averages = {}
        for column in columns:
            filtered_values = [row[column] for row in self.data if row[column] is not None and isinstance(row[column], (int, float))]
            if filtered_values:
                averages[column] = sum(filtered_values) / len(filtered_values)
        return averages

    def median(self, columns: Union[List[str], str] = "all") -> Dict[str, float]:
        """Compute the median value for numeric variables, omit None values."""
        if columns == "all":
            columns = [col for col in self.data[0].keys() if isinstance(self.data[0][col], (int, float, type(None)))]
        medians = {}
        for column in columns:
            filtered_values = [row[column] for row in self.data if row[column] is not None and isinstance(row[column], (int, float))]
            if filtered_values:
                medians[column] = statistics.median(filtered_values)
        return medians

    def percentile(self, columns: Union[List[str], str] = "all", percentile: int = 50) -> Dict[str, float]:
        """Compute the percentile value for numeric variables, default is 50% (median)."""
        if columns == "all":
            columns = [col for col in self.data[0].keys() if isinstance(self.data[0][col], (int, float, type(None)))]
        percentiles = {}
        for column in columns:
            filtered_values = [row[column] for row in self.data if row[column] is not None and isinstance(row[column], (int, float))]
            if filtered_values:
                percentiles[column] = statistics.quantiles(filtered_values, n=100)[percentile-1]
        return percentiles

    def type_and_mode(self, columns: Union[List[str], str] = "all") -> Dict[str, Union[Tuple[str, Any], Tuple[str, str]]]:
        """Compute the mode for variables, including variable type."""
        if columns == "all":
            columns = self.data[0].keys()
        modes = {}
        for column in columns:
            column_values = [row[column] for row in self.data if row[column] is not None]
            if column_values:
                if all(isinstance(value, (int, float)) for value in column_values):
                    mode_value = statistics.mode(column_values)
                    modes[column] = ('numeric', mode_value)
                else:
                    try:
                        mode_value = statistics.mode(column_values)
                        modes[column] = ('categorical', mode_value)
                    except statistics.StatisticsError:
                        modes[column] = ('categorical', 'No mode found')
        return modes


@dataclass
class DescriptorNumpy:
    """Class for summarizing and describing real estate data using NumPy."""
    data: np.ndarray  # Assuming data is a structured NumPy array

    def none_ratio(self, columns=None):
        """Compute the ratio of None (or np.nan for NumPy) values per column."""
        if columns is None:
            columns = self.data.dtype.names
        none_ratios = {}
        for column in columns:
            column_data = self.data[column]
            none_count = np.count_nonzero(np.isnan(column_data))
            total_count = column_data.shape[0]
            none_ratios[column] = none_count / total_count
        return none_ratios

    def average(self, columns=None):
        """Compute the average value for numeric variables, omit None (np.nan) values."""
        if columns is None:
            columns = self.data.dtype.names
        averages = {}
        for column in columns:
            column_data = self.data[column]
            if np.issubdtype(column_data.dtype, np.number):
                valid_data = column_data[~np.isnan(column_data)]
                if valid_data.size > 0:
                    averages[column] = np.mean(valid_data)
        return averages

    def median(self, columns=None):
        """Compute the median value for numeric variables, omit None (np.nan) values."""
        if columns is None:
            columns = self.data.dtype.names
        medians = {}
        for column in columns:
            column_data = self.data[column]
            if np.issubdtype(column_data.dtype, np.number):
                valid_data = column_data[~np.isnan(column_data)]
                if valid_data.size > 0:
                    medians[column] = np.median(valid_data)
        return medians

    def percentile(self, columns=None, percentile=50):
        """Compute the specified percentile value for numeric variables."""
        if columns is None:
            columns = self.data.dtype.names
        percentiles = {}
        for column in columns:
            column_data = self.data[column]
            if np.issubdtype(column_data.dtype, np.number):
                valid_data = column_data[~np.isnan(column_data)]
                if valid_data.size > 0:
                    percentiles[column] = np.percentile(valid_data, percentile)
        return percentiles

    def type_and_mode(self, columns=None):
        """Compute the mode and type for variables."""
        if columns is None:
            columns = self.data.dtype.names
        types_and_modes = {}
        for column in columns:
            column_data = self.data[column]
            if column_data.size > 0:
                types_and_modes[column] = (column_data.dtype, np.nan if np.isnan(column_data).all() else np.nanmode(column_data))
        return types_and_modes




