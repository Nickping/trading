
from datetime import datetime
import pandas as pd
from env.endpoints import DOMESTIC_DAILY_ENDPOINT
from env.tr_id import TrID
from network.request import request_with_logging
from env.config import get_domestic_params
from env.config import get_default_headers
from analyze.analyze_core import calculate_rsi, calculate_bollinger_bands


def analyze_domestic_stock(name: str, code: str):
    url = DOMESTIC_DAILY_ENDPOINT
    params = get_domestic_params(code)
    headers = get_default_headers()
    headers["tr_id"] = TrID.DOMESTIC.value

    data = request_with_logging(
        url=url, method="GET", params=params, headers=headers)
    candles = data.get("output2", [])

    if len(candles) < 21:
        return f"{name} 📉 일봉 데이터 부족 ({len(candles)}개)"

    df = pd.DataFrame(candles)
    df = df.sort_values("stck_bsop_date")
    df["close"] = df["stck_clpr"].astype(float)

    close = df["close"]
    rsi = calculate_rsi(close)
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
        date = datetime.strptime(row["stck_bsop_date"], "%Y%m%d").date()
        try:
            if (
                row["prev_close"] < row["prev_lower"] and
                row["close"] > row["lower"] and
                row["rsi"] < 35
            ):
                results.append(
                    f"🟢 매수 조건 만족: {date} | 종가: {row['close']} | RSI: {row['rsi']:.2f} {name} {code}")
            elif (
                row["prev_close"] > row["prev_upper"] and
                row["close"] < row["upper"] and
                row["rsi"] > 65
            ):
                results.append(
                    f"🔴 매도 조건 만족: {date} | 종가: {row['close']} | RSI: {row['rsi']:.2f} {name} {code}")
        except:
            continue

    if not results:
        return f"📊 {name} ({code})\n⚪ 2025년 이후 전략 조건 만족일 없음"
    return f"📊 {name} ({code})\n" + "\n".join(results)
