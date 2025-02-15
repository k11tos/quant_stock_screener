import pandas as pd
import logging

logger = logging.getLogger(__name__)

def filter_stocks(df):
    """소형 성장 가치주 필터링"""
    filtered_df = df[
        (df["ROIC"] >= 0.15) &
        (df["Debt/Equity"] <= 50) &
        (df["Market Cap"] <= df["Market Cap"].quantile(0.2))  # Small-cap 하위 20%
    ]
    return filtered_df
