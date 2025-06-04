from datetime import datetime
from analyze.analyze_domestic import analyze_domestic_stock
from analyze.analyze_foreign import analyze_foreign_stock
from env.config import DOMESTIC_STOCKS, FOREIGN_STOCKS
from network.broadcast import send_email
from network.broadcast import send_telegram_message
from env.secrets import EMAIL_CONFIG
from env.load_local import load_domestic_stocks, load_foreign_stocks
import schedule
import time
import re


# 종목 로딩
def main():
    DOMESTIC_STOCKS = load_domestic_stocks()
    FOREIGN_STOCKS = load_foreign_stocks()

    today = datetime.now().strftime("%Y-%m-%d")
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    messages = [f"⏰ [MCP 알림] {timestamp} 기준 전략 점검 결과\n"]

    summarize = [f"⚡️요약 정보\n"]
    has_summary = False

    # for stock in DOMESTIC_STOCKS:
    #     result = analyze_domestic_stock(
    #         stock["name"], stock["symbol"]) + "\n\n"
    #     matched = contains_today_alert(summarize, today, result)
    #     has_summary = has_summary or matched
    #     messages.append(result)
    #     print(result)

    for stock in FOREIGN_STOCKS:
        result = analyze_foreign_stock(stock["name"], stock["symbol"]) + "\n\n"
        matched = contains_today_alert(summarize, today, result)
        has_summary = has_summary or matched
        messages.append(result)
        print(result)

    if not has_summary:
        summarize.append("💬 현재 감지된 종목이 없습니다. ")

    # 결과 종합
    full_report = "\n".join(summarize) + "\n\n" + "\n".join(messages)
    print(full_report)

    # if has_summary:
    # 이메일 전송
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
    pattern = rf"(🟢 매수 조건 만족|🔴 매도 조건 만족): {today} \| 종가: ([0-9.]+) \| RSI: ([0-9.]+)"
    match = re.search(pattern, text)
    if match:
        summaries.append(match.group(0))
        return True

    return False


# 최초 실행
main()

# 60분마다 반복
schedule.every(60).minutes.do(main)

# 루프 실행
while True:
    schedule.run_pending()
    time.sleep(10)
