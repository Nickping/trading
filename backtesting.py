import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
import requests
from datetime import datetime
# from analyze.analyze_domestic import get_domestic_chart_data
from env.secrets import APP_SECRET, APP_KEY, get_token

# ✅ 해외 주식 차트 데이터 함수


DOMESTIC_STOCKS = [
    {"name": "삼성전자", "symbol": "005930"},
    {"name": "카카오뱅크", "symbol": "323410"},
    {"name": "네이버", "symbol": "035420"},
    {"name": "카카오", "symbol": "035720"},
    {"name": "SK이노베이션", "symbol": "096770"},
    {"name": "SK텔레콤", "symbol": "017670"},
    {"name": "SK하이닉스", "symbol": "000660"},
    {"name": "삼성전자(우)", "symbol": "005935"},
    {"name": "두산에너빌러티", "symbol": "034020"},
    {"name": "삼성중공업", "symbol": "010140"},
    {"name": "현대차", "symbol": "005380"},
    {"name": "HD Energy solution", "symbol": "322000"}
]

FOREIGN_STOCKS = [
    {"name": "테슬라", "symbol": "TSLA"},
    {"name": "엔비디아", "symbol": "NVDA"},
    {"name": "QQQ", "symbol": "QQQ"},
    {"name": "SPY", "symbol": "SPY"},
    {"name": "팔란티어", "symbol": "PLTR"},
    {"name": "애플", "symbol": "AAPL"},
    {"name": "알파벳A", "symbol": "GOOGL"},
    {"name": "코카콜라", "symbol": "KO"},
    {"name": "마이크로소프트", "symbol": "MSFT"},
    {"name": "메타", "symbol": "META"},
    {"name": "월마트", "symbol": "WMT"},
    {"name": "엑슨모빌", "symbol": "XOM"},
    {"name": "아마존", "symbol": "AMZN"}
]


def get_foreign_chart(symbol, start, end, token, appkey, appsecret):
    url = "https://openapi.koreainvestment.com:9443/uapi/overseas-price/v1/quotations/inquire-daily-chartprice"
    headers = {
        "authorization": get_token(),
        "appkey": APP_KEY,
        "appsecret": APP_SECRET,
        "tr_id": "FHKST03030100"
    }
    params = {
        "FID_COND_MRKT_DIV_CODE": "N",
        "FID_INPUT_ISCD": symbol,
        "FID_INPUT_DATE_1": start,
        "FID_INPUT_DATE_2": end,
        "FID_PERIOD_DIV_CODE": "D"
    }
    res = requests.get(url, headers=headers, params=params)
    res_json = res.json()
    # st.write("✅ API 응답 구조 확인", res_json)

    output2 = res_json.get("output2", [])
    if not output2:
        raise ValueError("❌ 해외 종목의 일봉 데이터가 없습니다.")

    df = pd.DataFrame(output2)
    if "stck_bsop_date" in df.columns:
        df["date"] = pd.to_datetime(df["stck_bsop_date"])
    elif "xymd" in df.columns:
        df["date"] = pd.to_datetime(df["xymd"])
    else:
        raise ValueError("❌ 날짜 필드가 응답에 존재하지 않습니다.")

    if "clos" in df.columns:
        df["close"] = df["clos"].astype(float)
    elif "ovrs_nmix_prpr" in df.columns:
        df["close"] = df["ovrs_nmix_prpr"].astype(float)
    else:
        raise ValueError("❌ 종가 필드가 응답에 존재하지 않습니다.")

    return df.sort_values("date")

# ✅ 국내 주식 차트 데이터 함수


def get_domestic_chart(symbol, start, end, token, appkey, appsecret):
    url = "https://openapi.koreainvestment.com:9443/uapi/domestic-stock/v1/quotations/inquire-daily-itemchartprice"
    headers = {
        "authorization": get_token(),
        "appkey": APP_KEY,
        "appsecret": APP_SECRET,
        "tr_id": "FHKST03010100"
    }

    params = {
        "fid_cond_mrkt_div_code": "J",
        "fid_input_iscd": symbol,
        "fid_input_date_1": start,
        "fid_input_date_2": end,
        "fid_period_div_code": "D",
        "fid_org_adj_prc": "1"
    }
    res = requests.get(url, headers=headers, params=params)
    res_json = res.json()
    # st.write("✅ API 응답 구조 확인", res_json)

    output2 = res_json.get("output2", [])
    if not output2:
        raise ValueError("❌ 국내 종목의 일봉 데이터가 없습니다.")

    df = pd.DataFrame(output2)
    df["date"] = pd.to_datetime(df["stck_bsop_date"])
    df["close"] = df["stck_clpr"].astype(float)
    return df.sort_values("date")

# 📊 지표 계산 함수


def compute_indicators(df):
    df["ma20"] = df["close"].rolling(window=20).mean()
    df["std20"] = df["close"].rolling(window=20).std()
    df["upper"] = df["ma20"] + 2 * df["std20"]
    df["lower"] = df["ma20"] - 2 * df["std20"]
    df["prev_close"] = df["close"].shift(1)
    df["prev_upper"] = df["upper"].shift(1)
    df["prev_lower"] = df["lower"].shift(1)

    delta = df["close"].diff()
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)
    avg_gain = gain.rolling(window=14).mean()
    avg_loss = loss.rolling(window=14).mean()
    rs = avg_gain / avg_loss
    df["rsi"] = 100 - (100 / (1 + rs))
    return df


# 📈 전략 시각화 및 수익률 계산 함수
def plot_strategy(df, name):
    buy_signals = []
    sell_signals = []
    trades = []
    shares = 0
    total_invested = 0
    cash = 0  # 매도 후 남는 현금

    for i in range(1, len(df)):
        row = df.iloc[i]
        prev = df.iloc[i - 1]
        date = row["date"]
        price = row["close"]

        # 매수 조건
        if (
            prev["close"] < prev["lower"]
            and row["close"] > row["lower"]
            and row["rsi"] < 35
        ):
            qty = 1000000 // price
            cost = qty * price
            if qty > 0:
                shares += qty
                total_invested += cost
                buy_signals.append((date, price))
                trades.append(("매수", date, price, qty))

        # 매도 조건
        elif (
            prev["close"] > prev["upper"]
            and row["close"] < row["upper"]
            and row["rsi"] > 65
        ):
            if shares > 0:
                proceeds = shares * price
                cash += proceeds
                sell_signals.append((date, price))
                trades.append(("매도", date, price, shares))
                shares = 0

    # 현재가 기준 자산 평가
    last_price = df.iloc[-1]["close"]
    total_value = cash + shares * last_price
    profit = total_value - total_invested
    profit_pct = (profit / total_invested * 100) if total_invested else 0

    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(df["date"], df["close"], label="종가")
    ax.plot(df["date"], df["upper"], "--", label="상단 밴드")
    ax.plot(df["date"], df["lower"], "--", label="하단 밴드")

    if buy_signals:
        dates, prices = zip(*buy_signals)
        ax.scatter(dates, prices, marker="^",
                   color="green", label="매수", zorder=5)
    if sell_signals:
        dates, prices = zip(*sell_signals)
        ax.scatter(dates, prices, marker="v",
                   color="red", label="매도", zorder=5)

    ax.set_title(f"{name} 전략 시각화")
    ax.legend()
    ax.grid()
    st.pyplot(fig)

    st.markdown("### 💹 수익률 분석")
    st.write(f"총 투자금액: {total_invested:,.0f}원")
    st.write(f"최종 자산: {total_value:,.0f}원")
    st.write(f"총 수익: {profit:,.0f}원 ({profit_pct:.2f}%)")
    st.write(f"총 매수 횟수: {len([t for t in trades if t[0]=='매수'])}")
    st.write(f"총 매도 횟수: {len([t for t in trades if t[0]=='매도'])}")

    # 거래 내역 테이블
    st.markdown("### 📋 거래 내역")
    if trades:
        df_trades = pd.DataFrame(trades, columns=["구분", "일자", "가격", "수량"])
        df_trades["일자"] = pd.to_datetime(df_trades["일자"]).dt.date
        st.dataframe(df_trades)
    else:
        st.write("거래 내역이 없습니다.")

# 📈 전략 시각화 및 수익률 계산 함수


def main():
    st.title("📊 장 마감 기준 백테스트 (국내/해외)")
    market = st.radio("시장 선택", ["국내", "해외"])

    stock_list = DOMESTIC_STOCKS if market == "국내" else FOREIGN_STOCKS
    stock_options = [f"{s['name']} ({s['symbol']})" for s in stock_list]
    selected = st.selectbox("분석할 종목 선택", options=stock_options)

    if st.button("✅ 실행"):
        name, code = selected.split(" (")
        code = code.strip(")")

        today = datetime.now().strftime("%Y%m%d")
        start = "20250101"

        if market == "국내":
            df = get_domestic_chart(
                code, start, today, get_token(), APP_KEY, APP_SECRET)
        else:
            df = get_foreign_chart(
                code, start, today, get_token(), APP_KEY, APP_SECRET)

        df["date"] = pd.to_datetime(df["date"])
        df = df.sort_values("date").reset_index(drop=True)

        df = compute_indicators(df)
        plot_strategy(df, name)


if __name__ == "__main__":
    main()
