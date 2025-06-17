
import streamlit as st
import pandas as pd
import requests
import matplotlib.pyplot as plt

# API 경로
API_URLS = {
    "국외": "http://localhost:7777/run_foreign",
    "국내": "http://localhost:7777/run_domestic"
}

# 타이틀
st.title("📈 주식 분석 시각화 대시보드")

# 시장 및 거래시간 선택
market = st.selectbox("📌 시장 선택", options=["국외", "국내"])
session = st.selectbox("⏰ 거래 시간", options=["장중", "장외"])
is_open = session == "장중"

def merge_buy_sell(buy_list, sell_list):
    buy_df = pd.DataFrame(buy_list or [])
    sell_df = pd.DataFrame(sell_list or [])

    # 💡 비어있는 경우에도 병합을 위해 컬럼 강제로 지정
    for df in [buy_df, sell_df]:
        if df.empty:
            df["name"] = pd.Series(dtype=str)
            df["code"] = pd.Series(dtype=str)
            df["date"] = pd.Series(dtype="datetime64[ns]")
        elif "date" in df.columns:
            df["date"] = pd.to_datetime(df["date"])

    merged = pd.merge(
        buy_df.rename(columns={"close": "close_buy", "rsi": "rsi_buy"}),
        sell_df.rename(columns={"close": "close_sell", "rsi": "rsi_sell"}),
        on=["name", "code", "date"],
        how="outer"
    )

    merged = merged.sort_values(by=["name", "code", "date"], ascending=[True, True, False])
    return merged


# 데이터 요청
try:
    response = requests.post(API_URLS[market], json={"is_open": is_open}, timeout=10)
    response.raise_for_status()
    data = response.json().get("result", {})
except Exception as e:
    st.error(f"❌ API 호출 실패: {e}")
    st.stop()
    

st.subheader("🔍 매수/매도 시그널 (highlighted)")
highlighted_data = data.get("highlighted", [])
highlighted_buy = [r for r in highlighted_data if r["type"] == "buy"]
highlighted_sell = [r for r in highlighted_data if r["type"] == "sell"]
highlighted_df = merge_buy_sell(highlighted_buy, highlighted_sell)

if not highlighted_df.empty:
    st.dataframe(highlighted_df, use_container_width=True)
else:
    st.write("❕ 해당 조건에 맞는 데이터 없음")

st.subheader("📅 지난 5일 매수/매도 종합")

past_buy = data.get("past_5days_buy", [])
past_sell = data.get("past_5days_sell", [])
past_df = merge_buy_sell(past_buy, past_sell)

if not past_df.empty:
    st.dataframe(past_df, use_container_width=True)
else:
    st.write("❕ 지난 5일 조건에 맞는 매수/매도 없음")


# flatten and filter records
records = []
for group in data.get("records", []):
    if isinstance(group, list):
        for entry in group:
            if isinstance(entry, dict) and "date" in entry:
                records.append(entry)

if records:
    df_all = pd.DataFrame(records)
    if "type" in df_all.columns:
        df_all = df_all[["name", "code", "date", "type", "close", "rsi"]]
        df_all["date"] = pd.to_datetime(df_all["date"])

        # ▶️ 피벗으로 buy/sell 나란히 배치
        pivot = df_all.pivot_table(
            index=["name", "code", "date"],
            columns="type",
            values=["close", "rsi"],
            aggfunc="first"
        ).reset_index()

        # ▶️ 컬럼 이름 평탄화
        pivot.columns = ["name", "code", "date", "close_buy", "close_sell", "rsi_buy", "rsi_sell"]

        # ▶️ 정렬: 종목 ➝ 날짜 내림차순
        pivot = pivot.sort_values(by=["name", "code", "date"], ascending=[True, True, False])

        st.subheader("🧾 종목별 매수/매도 요약")
        st.dataframe(pivot, use_container_width=True)
    else:
        st.write("❕ 타입 정보 없음")
else:
    st.info("⚠️ 전체 기록 데이터 없음")


# 디버그 출력
st.write("🧪 Raw Data 확인")
st.json(data)  # API 응답 전체 출력
