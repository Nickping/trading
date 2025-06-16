import streamlit as st
import pandas as pd
import requests
import matplotlib.pyplot as plt

# API 경로
API_URLS = {
    "국외": "http://localhost:7777/run_foreign",
    "국내": "http://localhost:7777/run_domestic"
}

# 사용자 선택
st.title("📈 주식 분석 시각화 대시보드")
market = st.selectbox("📌 시장 선택", options=["국외", "국내"])

# 데이터 요청
try:
    response = requests.post(API_URLS[market], json={}, timeout=10)
    response.raise_for_status()
    data = response.json().get("result", {})
except Exception as e:
    st.error(f"❌ API 호출 실패: {e}")
    st.stop()

# 하이라이트 데이터 표시
st.subheader("🔍 매수/매도 시그널 (highlighted)")
highlighted = pd.DataFrame(data.get("highlighted", []))
if not highlighted.empty:
    st.dataframe(highlighted)
else:
    st.write("❕ 해당 조건에 맞는 데이터 없음")

# 지난 5일 매수/매도
col1, col2 = st.columns(2)

with col1:
    st.subheader("📅 지난 5일 매수")
    buy_df = pd.DataFrame(data.get("past_5days_buy", []))
    if not buy_df.empty:
        st.dataframe(buy_df)
    else:
        st.write("❕ 없음")

with col2:
    st.subheader("📅 지난 5일 매도")
    sell_df = pd.DataFrame(data.get("past_5days_sell", []))
    if not sell_df.empty:
        st.dataframe(sell_df)
    else:
        st.write("❕ 없음")


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
        df_all = df_all.sort_values(by="date", ascending=False)
    st.dataframe(df_all, use_container_width=True)
else:
    st.info("⚠️ 전체 기록 데이터 없음")