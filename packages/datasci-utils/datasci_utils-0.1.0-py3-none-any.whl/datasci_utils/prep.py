'''
This module preprocesses raw time series data into more manageable datasets.

The module provides functions to build time-based datasets (monthly, weekly, 
daily) from raw time series data. Each function can optionally filter data for 
a specific store.

Functions:
    build_monthly_dataset: Aggregates data into monthly intervals
    build_weekly_dataset: Aggregates data into weekly intervals
    build_daily_dataset: Aggregates data into daily intervals
'''
from typing import Optional
import pandas as pd

def build_monthly_dataset(df: pd.DataFrame, store: Optional[str] = None) -> pd.DataFrame:
    """
    Build a dataset aggregated by month from the input DataFrame.

    Args:
        df (pd.DataFrame): Input DataFrame containing time series data
        store (Optional[str], optional): Store identifier to filter the data. 
            If None, includes all stores. Defaults to None.

    Returns:
        pd.DataFrame: DataFrame aggregated by month

    Example:
        >>> monthly_data = build_monthly_dataset(df, store="store001")
    """
    return (df
         .assign(
             year = lambda df_: df_["date"].dt.year,
             month = lambda df_: df_["date"].dt.month
         )
         .groupby(["year", "month", "shop_id", "item_id"])
         ["item_cnt_day"]
         .sum()
         .reset_index()
         .assign(date = lambda df_: df_["year"].astype("str") + "-" + df_["month"].astype("str").str.zfill(2) + "-01")
         .assign(date = lambda df_: pd.to_datetime(df_["date"]))
         .loc[:, ["year", "month", "shop_id", "item_id", "item_cnt_day"]]
         .sort_values(["shop_id", "item_id", "year", "month"])
    )

def build_weekly_dataset(df: pd.DataFrame, store: Optional[str] = None) -> pd.DataFrame:
    """
    Build a dataset aggregated by week from the input DataFrame.

    Args:
        df (pd.DataFrame): Input DataFrame containing time series data
        store (Optional[str], optional): Store identifier to filter the data. 
            If None, includes all stores. Defaults to None.

    Returns:
        pd.DataFrame: DataFrame aggregated by week

    Example:
        >>> weekly_data = build_weekly_dataset(df, store="store001")
    """
    return df

def build_daily_dataset(df: pd.DataFrame, store: Optional[str] = None) -> pd.DataFrame:
    """
    Build a dataset aggregated by day from the input DataFrame.

    Args:
        df (pd.DataFrame): Input DataFrame containing time series data
        store (Optional[str], optional): Store identifier to filter the data. 
            If None, includes all stores. Defaults to None.

    Returns:
        pd.DataFrame: DataFrame aggregated by day

    Example:
        >>> daily_data = build_daily_dataset(df, store="store001")
    """
    return df
