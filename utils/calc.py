# utils/calc.py
import os
import pandas as pd
import numpy as np

def percent_spread(a, b):
    """
    Percent spread relative to midpoint: 100 * |a-b| / ((a+b)/2)
    Returns None if either price is missing.
    """
    if a is None or b is None:
        return None
    mid = (a + b) / 2.0
    if mid == 0:
        return None
    return abs(a - b) / mid * 100.0

def detect_arbitrage(a, b, threshold_pct=0.25):
    """
    Returns (bool, pct) whether percent spread >= threshold_pct.
    """
    pct = percent_spread(a, b)
    if pct is None:
        return False, None
    return pct >= threshold_pct, pct

def append_price_row(row: dict, csv_path="data/prices.csv"):
    """
    Appends a dict row to csv_path. Creates file with header if not exists.
    row example: {"timestamp": "...", "BTC_binance":123, "BTC_coinbase":124, ...}
    """
    os.makedirs(os.path.dirname(csv_path), exist_ok=True)
    df = pd.DataFrame([row])
    header = not os.path.exists(csv_path)
    df.to_csv(csv_path, mode='a', index=False, header=header)

def load_and_correlate(csv_path="data/prices.csv", exchange='binance'):
    """
    Load the CSV, pick columns ending with _binance or _coinbase,
    compute log returns and return their correlation matrix.
    """
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"{csv_path} not found. Run the tracker (main.py) first.")
    df = pd.read_csv(csv_path, parse_dates=['timestamp'])
    suffix = "_binance" if exchange == 'binance' else "_coinbase"
    cols = [c for c in df.columns if c.endswith(suffix)]
    if not cols:
        raise ValueError("No columns found for exchange: " + exchange)
    prices = df[cols].copy()
    # rename columns to just asset tickers (drop suffix)
    prices.columns = [c.replace(suffix, '') for c in cols]
    # compute log returns, drop NA
    returns = np.log(prices).diff().dropna()
    if returns.empty:
        raise ValueError("Not enough data points to compute returns. Wait for more data.")
    corr = returns.corr()
    return corr
