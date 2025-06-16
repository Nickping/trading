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
    results = []
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
        return results.append({
            "name": name,
            "code": symbol,
            "error": "60분봉 데이터 부족"
        })


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

    
    for _, row in df.iterrows():
        date = row["date"].date()
        try:
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
            
            if is_buy_condition:
                results.append({
                    "name": name,
                    "code": symbol,
                    "date": date,
                    "type": "buy",
                    "close": round(row["close"], 2),
                    "rsi": round(row["rsi"], 2)
                })

            elif is_sell_condition:
                results.append({
                    "name": name,
                    "code": symbol,
                    "date": date,
                    "type": "sell",
                    "close": round(row["close"], 2),
                    "rsi": round(row["rsi"], 2)
                })

        except:
            continue
        return results


# Stochastic RSI 사용
def analyze_foreign_stock_for_opened(name: str, symbol: str):
    results = []
    url = FOREIGN_DAILY_ENDPOINT
    params = get_foreign_params(symbol)

    headers = get_default_headers()
    headers["tr_id"] = TrID.FOREIGN.value

    data = request_with_logging(
        url=url, method="GET", params=params, headers=headers)
    candles = data.get("output2", [])

    if len(candles) < 21:
        return [{
            "name": name,
            "code": symbol,
            "error": "60분봉 데이터 부족"
        }]

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
    
    for _, row in df.iterrows():
        date = row["date"].date()
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
            
            # print(f"analyze_foreign_stock_for_opened is_buy_condition: {is_buy_condition}, is_sell_condition: {is_sell_condition}")
            
            if is_buy_condition:
                results.append({
                    "name": name,
                    "code": symbol,
                    "date": date,
                    "type": "buy",
                    "close": round(row["close"], 2),
                    "rsi": round(row["stoch_rsi"], 2)
                })

            elif is_sell_condition:
                results.append({
                    "name": name,
                    "code": symbol,
                    "date": date,
                    "type": "sell",
                    "close": round(row["close"], 2),
                    "rsi": round(row["stoch_rsi"], 2)
                })

        except:
            continue
    cleaned_results = [group for group in results if group is not None]
    return cleaned_results


# 60 분봉, RSI 사용
def analyze_foreign_stock_for_opened_within_60min_RSI(name: str, symbol: str, excd="NAS"):
    results = []
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
        return [{
            "name": name,
            "code": symbol,
            "error": "60분봉 데이터 부족"
        }]


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
            
            # print(f"analyze_foreign_stock_for_opened_within_60min_RSI is_buy_condition: {is_buy_condition}, is_sell_condition: {is_sell_condition}")
            
            if is_buy_condition:
                results.append({
                    "name": name,
                    "code": symbol,
                    "date": date,
                    "type": "buy",
                    "close": round(row["close"], 2),
                    "rsi": round(row["rsi"], 2)
                })

            elif is_sell_condition:
                results.append({
                    "name": name,
                    "code": symbol,
                    "date": date,
                    "type": "sell",
                    "close": round(row["close"], 2),
                    "rsi": round(row["rsi"], 2)
                })

        except:
            continue
    cleaned_results = [group for group in results if group is not None]
    return cleaned_results

