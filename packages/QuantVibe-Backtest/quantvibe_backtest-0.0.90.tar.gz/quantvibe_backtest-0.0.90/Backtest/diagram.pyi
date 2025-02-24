import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from typing import List, Tuple

def plot_single_diagram(df: pd.DataFrame, report_df: pd.DataFrame) -> None:
    ...

def plot_heatmap(report_df: pd.DataFrame) -> None:
    ...

def plot_data_spread(df: pd.DataFrame) -> None:
    ...

def plot_correlation(file_paths: List[Tuple[str, float]], start_time: str, end_time: str) -> None:
    ...

def plot_combined_equity(file_paths: List[Tuple[str, float]], start_time: str, end_time: str) -> None:
    ...
