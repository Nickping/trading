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


# 하루 전 기준으로 하기때문에 과거 이력 보긴 좋음..
def calculate_rsi(close_prices, period=14, shift=False):
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
    if shift:
        rsi = rsi.shift(1)

    return rsi

# Stochastic RSI. 0.2 < 과매도, 0.8 > 과매수


def calculate_stoch_rsi(close_prices: pd.Series, rsi_period: int = 14, stoch_period: int = 14) -> pd.Series:
    # Step 1: RSI 계산 (shift 없이 실시간 대응)
    delta = close_prices.diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)

    avg_gain = gain.ewm(alpha=1/rsi_period,
                        min_periods=rsi_period, adjust=False).mean()
    avg_loss = loss.ewm(alpha=1/rsi_period,
                        min_periods=rsi_period, adjust=False).mean()

    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))

    # Step 2: Stochastic 처리
    min_rsi = rsi.rolling(window=stoch_period).min()
    max_rsi = rsi.rolling(window=stoch_period).max()

    stoch_rsi = (rsi - min_rsi) / (max_rsi - min_rsi)
    return stoch_rsi


def calculate_bollinger_bands(close_prices, window=20, num_std=2):
    sma = close_prices.rolling(window=window).mean()
    std = close_prices.rolling(window=window).std()
    upper_band = sma + num_std * std
    lower_band = sma - num_std * std
    return sma, upper_band, lower_band
