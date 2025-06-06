# analyze/analyze_foreign.py

from datetime import datetime
import pandas as pd
from env.endpoints import FOREIGN_DAILY_ENDPOINT, FOREIGN_TIME_ITEM_CHART_PRICE
from env.tr_id import TrID
from network.request import request_with_logging
from env.config import get_foreign_params
from env.config import get_default_headers
from analyze.analyze_core import calculate_rsi, calculate_bollinger_bands, calculate_stoch_rsi
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def analyze_foreign_stock_for_closed(name: str, symbol: str):
    url = FOREIGN_DAILY_ENDPOINT
    params = get_foreign_params(symbol)

    headers = get_default_headers()
    print(f"❤️ before header {headers}")
    headers["tr_id"] = TrID.FOREIGN.value

    data = request_with_logging(
        url=url, method="GET", params=params, headers=headers)
    print(f"❤️ after header {headers}")
    candles = data.get("output2", [])

    if len(candles) < 21:
        return f"{name} 📉 일봉 데이터 부족 ({len(candles)}개)"

    df = pd.DataFrame(candles)
    df = df.sort_values("stck_bsop_date")
    df["close"] = df["ovrs_nmix_prpr"].astype(float)
    df["date"] = pd.to_datetime(df["stck_bsop_date"])

    close = df["close"]
    rsi = calculate_rsi(close, shift=True)
    sma, upper, lower = calculate_bollinger_bands(close)

    df = df.iloc[-len(rsi):].copy()
    df["rsi"] = rsi.values
    df["upper"] = upper.values
    df["lower"] = lower.values
    df["prev_close"] = df["close"].shift(1)
    df["prev_upper"] = df["upper"].shift(1)
    df["prev_lower"] = df["lower"].shift(1)

    results = []
    for _, row in df.iterrows():
        date = row["date"].date()
        try:
            if (
                row["prev_close"] < row["prev_lower"] and
                row["close"] > row["lower"] and
                row["rsi"] < 35
            ):
                results.append(
                    f"🟢 매수 조건 만족: {date} | 종가: {row['close']:.2f} | RSI: {row['rsi']:.2f} {name} {symbol}")
            elif (
                row["prev_close"] > row["prev_upper"] and
                row["close"] < row["upper"] and
                row["rsi"] > 65
            ):
                results.append(
                    f"🔴 매도 조건 만족: {date} | 종가: {row['close']:.2f} | RSI: {row['rsi']:.2f} {name} {symbol}")
        except:
            continue

    if not results:
        return f"📊 {name} ({symbol})\n⚪ 전략 조건 만족일 없음"
    return f"📊 {name} ({symbol})\n" + "\n".join(results)


# Stochastic RSI 사용
def analyze_foreign_stock_for_opened(name: str, symbol: str):
    url = FOREIGN_DAILY_ENDPOINT
    params = get_foreign_params(symbol)

    headers = get_default_headers()
    headers["tr_id"] = TrID.FOREIGN.value

    data = request_with_logging(
        url=url, method="GET", params=params, headers=headers)
    candles = data.get("output2", [])

    if len(candles) < 21:
        return f"{name} 📉 일봉 데이터 부족 ({len(candles)}개)"

    df = pd.DataFrame(candles)
    df = df.sort_values("stck_bsop_date")
    df["close"] = df["ovrs_nmix_prpr"].astype(float)
    df["date"] = pd.to_datetime(df["stck_bsop_date"])

    close = df["close"]
    stoch_rsi = calculate_stoch_rsi(close)
    sma, upper, lower = calculate_bollinger_bands(close)

    df = df.iloc[-len(stoch_rsi):].copy()
    df["stoch_rsi"] = stoch_rsi.values
    df["upper"] = upper.values
    df["lower"] = lower.values
    df["prev_close"] = df["close"].shift(1)
    df["prev_upper"] = df["upper"].shift(1)
    df["prev_lower"] = df["lower"].shift(1)

    results = []
    for _, row in df.iterrows():
        date = row["date"].date()
        try:
            if (
                row["prev_close"] < row["prev_lower"] and
                row["close"] > row["lower"] and
                row["stoch_rsi"] < 0.3
            ):
                results.append(
                    f"🟢 매수 조건 만족: {date} | 종가: {row['close']:.2f} | StochRSI: {row['stoch_rsi']:.2f} {name} {symbol}")
            elif (
                row["prev_close"] > row["prev_upper"] and
                row["close"] < row["upper"] and
                row["stoch_rsi"] > 0.7
            ):
                results.append(
                    f"🔴 매도 조건 만족: {date} | 종가: {row['close']:.2f} | StochRSI: {row['stoch_rsi']:.2f} {name} {symbol}")
        except:
            continue

    if not results:
        return f"📊 {name} ({symbol})\n⚪ 전략 조건 만족일 없음"
    return f"📊 {name} ({symbol})\n" + "\n".join(results)


# 60 분봉, RSI 사용
def analyze_foreign_stock_for_opened_within_60min_RSI(name: str, symbol: str, excd="NAS"):
    url = FOREIGN_TIME_ITEM_CHART_PRICE
    params = {
        "AUTH": "",
        "EXCD": excd,
        "SYMB": symbol,
        "NMIN": "60",  # 60분봉
        "PINC": "1",
        "NEXT": "",
        "NREC": "120",  # 최대 120개
        "FILL": "",
        "KEYB": ""
    }

    headers = get_default_headers()
    headers["tr_id"] = "HHDFS76950200"  # 60분봉 요청용 (실제 ID 확인 필요)

    data = request_with_logging(
        url=url, method="GET", params=params, headers=headers)
    candles = data.get("output2", [])

    if len(candles) < 21:
        return f"{name} 📉 60분봉 데이터 부족 ({len(candles)}개)"

    df = pd.DataFrame(candles)
    df = df.sort_values(["tymd", "xhms"])
    df["close"] = df["last"].astype(float)
    df["date"] = pd.to_datetime(df["tymd"] + df["xhms"], format="%Y%m%d%H%M%S")
    df["date"] = pd.to_datetime(df["tymd"] + df["xhms"], format="%Y%m%d%H%M%S")

    close = df["close"]
    rsi = calculate_rsi(close, shift=False)
    sma, upper, lower = calculate_bollinger_bands(close)

    df = df.iloc[-len(rsi):].copy()
    df["rsi"] = rsi.values
    df["upper"] = upper.values
    df["lower"] = lower.values
    df["prev_close"] = df["close"].shift(1)
    df["prev_upper"] = df["upper"].shift(1)
    df["prev_lower"] = df["lower"].shift(1)

    results = []
    for _, row in df.iterrows():
        date = row["date"].strftime("%Y-%m-%d %H:%M")
        try:
            if (
                row["prev_close"] < row["prev_lower"] and
                row["close"] > row["lower"] and
                row["rsi"] < 40
            ):
                results.append(
                    f"🟢 매수 조건 만족: {date} | 종가: {row['close']:.2f} | RSI: {row['rsi']:.2f} {name} {symbol}")
            elif (
                row["prev_close"] > row["prev_upper"] and
                row["close"] < row["upper"] and
                row["rsi"] > 6
            ):
                results.append(
                    f"🔴 매도 조건 만족: {date} | 종가: {row['close']:.2f} | RSI: {row['rsi']:.2f} {name} {symbol}")
        except:
            continue

    if not results:
        return f"📊 {name} ({symbol})\n⚪ 전략 조건 만족일 없음"
    return f"📊 {name} ({symbol})\n" + "\n".join(results)
