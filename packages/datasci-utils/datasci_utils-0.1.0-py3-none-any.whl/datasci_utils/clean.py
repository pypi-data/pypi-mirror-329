'''
This module leverages cleaning functions for time series data.

The module provides utilities for cleaning and standardizing time series data,
with a focus on date formatting and validation. These functions help ensure
consistency in date representations across the dataset.

Functions:
    clean_date: Standardizes date string formats
'''
import os
from pathlib import Path
from typing import Optional
import pandas as pd


def clean_date(col: pd.Series) -> pd.Series:
    """
    Convert a pandas Series containing date strings into datetime objects using a specific format.

    Args:
        col (pd.Series): A pandas Series containing date strings in the format 'DD.MM.YYYY'

    Returns:
        pd.Series: A pandas Series with datetime objects

    Examples:
        >>> import pandas as pd
        >>> dates = pd.Series(['01.01.2023', '02.01.2023'])
        >>> clean_date(dates)
        0   2023-01-01
        1   2023-01-02
        dtype: datetime64[ns]

    Notes:
        - The input date strings must be in the format 'DD.MM.YYYY' (e.g., '01.01.2023')
        - Invalid date formats will raise ValueError
        - The function uses pandas.to_datetime with format='%d.%m.%Y'
    
    Raises:
        ValueError: If the dates in the series don't match the expected format
        TypeError: If the input is not a pandas Series
    """
    return pd.to_datetime(col, format = "%d.%m.%Y")


def export_to_parquet(df: pd.DataFrame, path: str, partition_cols: list = None) -> None:
    """
    Exports a pandas DataFrame to parquet format with optional partitioning.

    This function saves a DataFrame to a parquet file or directory, with support for
    partitioning based on specified columns. The output is compressed using gzip compression.

    Args:
        df (pd.DataFrame): The DataFrame to be exported to parquet format.
        path (str): The file path or directory where the parquet file(s) will be saved.
            If partitioning is used, this will be a directory path.
        partition_cols (list, optional): List of column names to use for partitioning the data.
            If provided, the data will be split into multiple parquet files based on
            unique combinations of values in these columns. Defaults to None.

    Returns:
        None

    Examples:
        >>> df = pd.DataFrame({'col1': [1, 2], 'col2': ['a', 'b']})

        >>> # Export without partitioning
        >>> export_to_parquet(df, 'data.parquet')

        >>> # Export with partitioning by 'col2'
        >>> export_to_parquet(df, 'data_dir', partition_cols=['col2'])

    Notes:
        - The function uses gzip compression by default
        - When using partition_cols, the output will be a directory containing
          multiple parquet files organized in a directory structure based on
          the partition columns
    """

    if partition_cols is None:
        df.to_parquet(path, index=False, compression="gzip")
    else:
        df.to_parquet(path, index=False, compression="gzip", partition_cols=partition_cols)


    if partition_cols is None:
        df.to_parquet(path, index = False, compression="gzip")
    else:
        df.to_parquet(path, index = False, compression="gzip", partition_cols=partition_cols)