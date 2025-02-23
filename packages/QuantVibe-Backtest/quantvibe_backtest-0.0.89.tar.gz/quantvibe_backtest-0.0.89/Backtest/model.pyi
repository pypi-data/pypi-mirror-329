import pandas as pd
import numpy as np

def mean_normalize_backtesting(
    df: pd.DataFrame, 
    rolling_window: int, 
    threshold: float, 
    fees: float, 
    sr_multiplier: float, 
    backtest_mode: str
) -> pd.DataFrame:
    ...

def mean_normalize(
    df: pd.DataFrame, 
    backtest_mode_list: list[str], 
    rolling_window_range: np.ndarray, 
    threshold_range: np.ndarray, 
    fees: float, 
    sr_multiplier: float
) -> None:
    ...

def bollinger_bands_backtesting(
    df: pd.DataFrame, 
    rolling_window: int, 
    multiplier: float, 
    fees: float, 
    sr_multiplier: float, 
    backtest_mode: str
) -> pd.DataFrame:
    ...

def bollinger_bands(
    df: pd.DataFrame, 
    backtest_mode_list: list[str], 
    rolling_window_range: np.ndarray, 
    threshold_range: np.ndarray, 
    fees: float, 
    sr_multiplier: float
) -> None:
    ...

def rsi_backtesting(
    df: pd.DataFrame, 
    rolling_window: int, 
    threshold: float, 
    fees: float, 
    sr_multiplier: float, 
    backtest_mode: str
) -> pd.DataFrame:
    ...

def rsi(
    df: pd.DataFrame, 
    backtest_mode_list: list[str], 
    rolling_window_range: np.ndarray, 
    threshold_range: np.ndarray, 
    fees: float, 
    sr_multiplier: float
) -> None:
    ...

def zscore_backtesting(
    df: pd.DataFrame, 
    rolling_window: int, 
    threshold: float, 
    fees: float, 
    sr_multiplier: float, 
    backtest_mode: str
) -> pd.DataFrame:
    ...

def zscore(
    df: pd.DataFrame, 
    backtest_mode_list: list[str], 
    rolling_window_range: np.ndarray, 
    threshold_range: np.ndarray, 
    fees: float, 
    sr_multiplier: float
) -> None:
    ...

def macd_backtesting(
    df: pd.DataFrame, 
    rolling_window1: int, 
    rolling_window2: int, 
    fees: float, 
    sr_multiplier: float
) -> pd.DataFrame:
    ...

def macd(
    df: pd.DataFrame, 
    rolling_window1: np.ndarray, 
    rolling_window2: np.ndarray, 
    fees: float, 
    sr_multiplier: float
) -> None:
    ...
