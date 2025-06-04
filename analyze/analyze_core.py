import pandas as pd
import numpy as np
from datetime import datetime


# def calculate_rsi(close_prices, period=14):
#     delta = close_prices.diff()
#     gain = np.where(delta > 0, delta, 0)
#     loss = np.where(delta < 0, -delta, 0)
#     avg_gain = pd.Series(gain).rolling(window=period).mean()
#     avg_loss = pd.Series(loss).rolling(window=period).mean()
#     rs = avg_gain / avg_loss
#     rsi = 100 - (100 / (1 + rs))
#     return rsi

def calculate_rsi(close_prices, period=14):
    delta = close_prices.diff()

    gain = np.where(delta > 0, delta, 0)
    loss = np.where(delta < 0, -delta, 0)

    gain_series = pd.Series(gain, index=close_prices.index)
    loss_series = pd.Series(loss, index=close_prices.index)

    avg_gain = gain_series.rolling(window=period).mean()
    avg_loss = loss_series.rolling(window=period).mean()

    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))

    # 핵심: 전날까지의 RSI로 정렬 (현재날짜에는 아직 반영되지 않은 값)
    rsi = rsi.shift(1)

    return rsi


def calculate_bollinger_bands(close_prices, window=20, num_std=2):
    sma = close_prices.rolling(window=window).mean()
    std = close_prices.rolling(window=window).std()
    upper_band = sma + num_std * std
    lower_band = sma - num_std * std
    return sma, upper_band, lower_band
