import pandas as pd
import numpy as np
from datetime import datetime


def calculate_rsi(close_prices, period=14):
    delta = close_prices.diff()
    gain = np.where(delta > 0, delta, 0)
    loss = np.where(delta < 0, -delta, 0)
    avg_gain = pd.Series(gain).rolling(window=period).mean()
    avg_loss = pd.Series(loss).rolling(window=period).mean()
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi


def calculate_bollinger_bands(close_prices, window=20, num_std=2):
    sma = close_prices.rolling(window=window).mean()
    std = close_prices.rolling(window=window).std()
    upper_band = sma + num_std * std
    lower_band = sma - num_std * std
    return sma, upper_band, lower_band


def get_domestic_params(code: str, start_date="20250101"):
    return {
        "fid_cond_mrkt_div_code": "J",
        "fid_input_iscd": code,
        "fid_input_date_1": start_date,
        "fid_input_date_2": datetime.now().strftime("%Y%m%d"),
        "fid_period_div_code": "D",
        "fid_org_adj_prc": "1",
        "fid_etc_cls_code": ""
    }


def get_foreign_params(symbol: str, start_date="20250101"):
    return {
        "FID_COND_MRKT_DIV_CODE": "N",
        "FID_INPUT_ISCD": symbol,
        "FID_INPUT_DATE_1": start_date,
        "FID_INPUT_DATE_2": datetime.now().strftime("%Y%m%d"),
        "FID_PERIOD_DIV_CODE": "D"
    }
