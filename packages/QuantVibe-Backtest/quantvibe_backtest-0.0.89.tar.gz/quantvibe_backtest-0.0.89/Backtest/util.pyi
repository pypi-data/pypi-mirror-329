import pandas as pd
import numpy as np
from typing import Optional
from datetime import datetime

def load_data(data_path: str, candle_path: str, start_time: datetime, end_time: datetime, shift_time: int) -> pd.DataFrame:
    """
    Load data from given CSV files, merge with candle data, and filter by time range.

    Args:
    - data_path (str): Path to the trading data CSV file.
    - candle_path (str): Path to the candle data CSV file.
    - start_time (datetime): Start time for filtering data.
    - end_time (datetime): End time for filtering data.
    - shift_time (int): Time shift adjustment for candle data.

    Returns:
    - pd.DataFrame: Merged DataFrame containing trading and candle data.
    """
    pass

def generate_report(df: pd.DataFrame, param1: str, param2: str, fees: float, sr_multiplier: float) -> dict:
    """
    Generate a report with key performance metrics based on trading data.

    Args:
    - df (pd.DataFrame): DataFrame containing trading data with position and price changes.
    - param1 (str): First parameter for reporting.
    - param2 (str): Second parameter for reporting.
    - fees (float): Transaction fees as a percentage.
    - sr_multiplier (float): Sharpe Ratio multiplier to adjust the time factor.

    Returns:
    - dict: Dictionary containing the performance metrics report.
    """
    pass
