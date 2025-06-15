from datetime import datetime, timedelta
from analyze.analyze_domestic import analyze_domestic_stock_for_closed, analyze_domestic_stock_for_opened
from analyze.analyze_foreign import analyze_foreign_stock_for_closed, analyze_foreign_stock_for_opened, analyze_foreign_stock_for_opened_within_60min_RSI
from env.config import DOMESTIC_STOCKS, FOREIGN_STOCKS
from utils.open_check import is_domestic_open, is_foreign_open
from network.broadcast import send_email
from network.broadcast import send_telegram_message
from env.secrets import EMAIL_CONFIG
from env.load_local import load_domestic_stocks, load_foreign_stocks
import re
import schedule
import time
import re


def main():
    DOMESTIC_STOCKS = load_domestic_stocks()
    FOREIGN_STOCKS = load_foreign_stocks()

    today = datetime.now().strftime("%Y-%m-%d")
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    messages = [f"⏰ [MCP 알림] {timestamp} 기준 전략 점검 결과\n"]
    summarize = [f"⚡️요약 정보\n"]
    has_summary = False

    is_dom_open = is_domestic_open()
    is_for_open = is_foreign_open()

    for stock in DOMESTIC_STOCKS:
        if is_dom_open:
            result = analyze_domestic_stock_for_opened(
                stock["name"], stock["symbol"])
        else:
            result = analyze_domestic_stock_for_closed(
                stock["name"], stock["symbol"])
        result += "\n\n"
        matched = contains_today_alert(summarize, today, result)
        has_summary = has_summary or matched
        messages.append(result)
        print(result)

    for stock in FOREIGN_STOCKS:
        if is_for_open:
            result = analyze_foreign_stock_for_opened_within_60min_RSI(
                stock["name"], stock["symbol"], stock["excd"])
        else:
            result = analyze_foreign_stock_for_closed(
                stock["name"], stock["symbol"])
        result += "\n\n"
        matched = contains_today_alert(summarize, today, result)
        has_summary = has_summary or matched
        messages.append(result)
        print(result)

    if not has_summary:
        summarize.append("💬 현재 감지된 종목이 없습니다. ")

    full_report = "\n".join(summarize) + "\n\n" + "\n".join(messages)
    print(full_report)

    if has_summary:
        send_email(
            subject=f"[MCP 알림] {timestamp} 전략 점검 결과",
            body=full_report,
            sender=EMAIL_CONFIG["sender"],
            recipient=EMAIL_CONFIG["recipient"],
            smtp_server=EMAIL_CONFIG["smtp_server"],
            smtp_port=EMAIL_CONFIG["smtp_port"],
            smtp_user=EMAIL_CONFIG["smtp_user"],
            smtp_password=EMAIL_CONFIG["smtp_password"]
        )
        send_telegram_message(full_report)


def contains_today_alert(summaries, today, text):
    # 어제 날짜도 포함
    yesterday = (datetime.strptime(today, "%Y-%m-%d") -
                 timedelta(days=1)).strftime("%Y-%m-%d")

    pattern_open = rf"(🟢 매수 조건 만족|🔴 매도 조건 만족): ({today}|{yesterday}) \d{{2}}:\d{{2}} \| 종가: ([0-9.]+) \| RSI: ([0-9.]+)"
    pattern_closed = rf"(🟢 매수 조건 만족|🔴 매도 조건 만족): ({today}|{yesterday}) \| 종가: ([0-9.]+) \| RSI: ([0-9.]+)"
    match = re.search(pattern_open, text) or re.search(pattern_closed, text)
    if match:
        # 종목명과 심볼은 텍스트 마지막 단어 2개라고 가정
        parts = text.strip().split()
        stock_info = " ".join(parts[-2:])  # 예: "카카오페이 377300"
        summaries.append(f"{stock_info}: {match.group(0)}")
        return True
    return False


# 최초 실행
main()

# 30분마다 반복
schedule.every(60).minutes.do(main)

# 루프 실행
while True:
    schedule.run_pending()
    time.sleep(10)
