import re
import pandas as pd
from pandas.api.types import is_datetime64_any_dtype

# Pre-compile a regex that captures three numeric groups in a date-like string
# e.g., "13.01.2013", "13-01-2013", etc.
_DATE_REGEX = re.compile(r'^\D*(\d{1,4})\D+(\d{1,4})\D+(\d{1,4})\D*$')


def is_day_first(series: pd.Series, sample_size: int = 1000) -> bool:
    """
    Determine if the date strings in `series` are day-first or month-first
    using a vectorized approach on a sampled subset.

    1. Drop NaNs and sample up to `sample_size` rows for performance.
    2. Vectorized regex-extract to capture the first, second, third numeric groups.
    3. If any row in that sample has `g1 > 12`, we conclude day-first.
    4. Otherwise, default to month-first.

    Args:
        series (pd.Series): Column containing date strings.
        sample_size (int): Max number of rows to sample when inferring day-first.

    Returns:
        bool: True if day-first is detected, otherwise False (month-first).
    """
    if is_datetime64_any_dtype(series):
        # Just skip guess logic if already parsed
        return False  # or True, or None, etc.

    non_null_series = series.dropna()
    if non_null_series.empty:
        # No data to guess from => default to month-first
        return False

    # Sample if we have more than sample_size rows
    if len(non_null_series) > sample_size:
        data_for_guess = non_null_series.sample(sample_size, random_state=0)
    else:
        data_for_guess = non_null_series

    # Vectorized extraction: each match yields up to 3 groups
    # If there's no match, extract returns NaN for that row
    extracted = data_for_guess.str.extract(_DATE_REGEX)

    # Convert groups to numeric; any invalid parse remains NaN
    # columns: 0 => g1, 1 => g2, 2 => g3
    extracted = extracted.apply(pd.to_numeric, errors='coerce')

    # If any row has g1 > 12, that row cannot be month-first => day-first
    if ((extracted[0] > 12) & (extracted[0] < 32)).any():
        return True
    return False