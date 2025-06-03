from datetime import datetime
from analyze.analyze_domestic import analyze_domestic_stock
from analyze.analyze_foreign import analyze_foreign_stock
from env.config import DOMESTIC_STOCKS, FOREIGN_STOCKS
# from notification.telegram import send_telegram_message
from network.broadcast import send_email
from env.secrets import EMAIL_CONFIG
import schedule
import time


def main():
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    messages = [f"⏰ [MCP 알림] {timestamp} 기준 전략 점검 결과\n"]

    # 국내 주식 분석
    for name, code in DOMESTIC_STOCKS.items():
        result = analyze_domestic_stock(name, code)
        messages.append(result + "\n")
        print(result)

    # 해외 주식 분석
    for stock in FOREIGN_STOCKS:
        result = analyze_foreign_stock(stock["name"], stock["symbol"])
        messages.append(result + "\n")
        print(result)

    # 결과 종합
    full_report = "\n".join(messages)
    print(full_report)

    # # 텔레그램 전송
    # send_telegram_message(full_report)

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


# 최초 실행
main()

# 60분마다 반복
schedule.every(60).minutes.do(main)

# 루프 실행
while True:
    schedule.run_pending()
    time.sleep(10)
