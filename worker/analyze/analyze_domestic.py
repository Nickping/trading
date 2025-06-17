
from datetime import datetime
import pandas as pd
from env.endpoints import DOMESTIC_DAILY_ENDPOINT
from env.tr_id import TrID
from network.request import request_with_logging
from env.config import get_domestic_params
from env.config import get_default_headers
from analyze.analyze_core import calculate_rsi, calculate_bollinger_bands, calculate_stoch_rsi


def analyze_domestic_stock_for_closed(name: str, code: str):
    results = []
    url = DOMESTIC_DAILY_ENDPOINT
    params = get_domestic_params(code)
    headers = get_default_headers()
    headers["tr_id"] = TrID.DOMESTIC.value

    data = request_with_logging(
        url=url, method="GET", params=params, headers=headers)
    candles = data.get("output2", [])

    if len(candles) < 21:
        return results.append({
            "name": name,
            "code": code,
            "error": "60분봉 데이터 부족"
        })


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
    
    print(f"df : {df}")

    
    for _, row in df.iterrows():
        date = datetime.strptime(row["stck_bsop_date"], "%Y%m%d").date()
        
        is_buy_condition = (
            row["prev_close"] < row["prev_lower"] and
            row["close"] > row["lower"] and
            row["rsi"] < 35
        )
        
        is_sell_condition = (
            row["prev_close"] > row["prev_upper"] and
            row["close"] < row["upper"] and
            row["rsi"] > 65
        )
        
        try:
            if is_buy_condition:
                results.append({
                    "name": name,
                    "code": code,
                    "date": date,
                    "type": "buy",
                    "close": round(row["close"], 2),
                    "rsi": round(row["rsi"], 2)
                })

            elif is_sell_condition:
                results.append({
                    "name": name,
                    "code": code,
                    "date": date,
                    "type": "sell",
                    "close": round(row["close"], 2),
                    "rsi": round(row["rsi"], 2)
                })
        except:
            continue

    cleaned_results = [group for group in results if group is not None]
    print(f"results : {results}")
    return cleaned_results


# Stochastic RSI 사용
def analyze_domestic_stock_for_opened(name: str, code: str):
    results = []
    url = DOMESTIC_DAILY_ENDPOINT
    params = get_domestic_params(code)
    headers = get_default_headers()
    headers["tr_id"] = TrID.DOMESTIC.value

    data = request_with_logging(
        url=url, method="GET", params=params, headers=headers)
    candles = data.get("output2", [])

    if len(candles) < 21:
        return results.append({
            "name": name,
            "code": code,
            "error": "60분봉 데이터 부족"
        })


    df = pd.DataFrame(candles)
    df = df.sort_values("stck_bsop_date")
    df["close"] = df["stck_clpr"].astype(float)

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

    print(f"df : {df}")
    
    for _, row in df.iterrows():
        date = datetime.strptime(row["stck_bsop_date"], "%Y%m%d").date()
        try:
            is_buy_condition = (
                row["prev_close"] < row["prev_lower"] and
                row["close"] > row["lower"] and
                row["stoch_rsi"] < 0.3
            )
        
            is_sell_condition = (
                row["prev_close"] > row["prev_upper"] and
                row["close"] < row["upper"] and
                row["stoch_rsi"] > 0.7
            )
            if is_buy_condition:
                results.append({
                    "name": name,
                    "code": code,
                    "date": date,
                    "type": "buy",
                    "close": round(row["close"], 2),
                    "rsi": round(row["stoch_rsi"], 2)
                })
                
            elif is_sell_condition:
                results.append({
                    "name": name,
                    "code": code,
                    "date": date,
                    "type": "sell",
                    "close": round(row["close"], 2),
                    "rsi": round(row["stoch_rsi"], 2)
                })

        except:
            continue
    print(f"results : {results}")
    cleaned_results = [group for group in results if group is not None]
    
    return cleaned_results
