from typing import Any

import pandas as pd

from .log import get_logger

logger = get_logger(__name__)


def filter_dataframe(df: pd.DataFrame, **kwargs: Any) -> pd.DataFrame:
    """
    Filters a Pandas DataFrame based on column-value pairs passed as keyword arguments.

    Parameters:
        df (pd.DataFrame): The input DataFrame to filter.
        **kwargs (Any): Column-value pairs for filtering. Only columns present in the DataFrame
                        will be considered, and `None` values are ignored.

    Returns:
        pd.DataFrame: A filtered DataFrame based on the conditions.

    Example:
        >>> data = {'A': [1, 2, 3], 'B': ['x', 'y', 'z']}
        >>> df = pd.DataFrame(data)
        >>> filtered_df = filter_dataframe(df, A=2, B='y')
        >>> print(filtered_df)
           A  B
        1  2  y
    """
    if not isinstance(df, pd.DataFrame):
        raise ValueError("The 'df' parameter must be a pandas DataFrame.")

    filtered_df = df.copy()

    for col, value in kwargs.items():
        if col in filtered_df.columns and value is not None:
            filtered_df = filtered_df[filtered_df[col] == value]

    return filtered_df
