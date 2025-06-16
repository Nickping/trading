
# 📁 app/send_email.py

import requests
from email.mime.text import MIMEText
from email.header import Header
from env.secrets import TELEGRAM_CONFIG
import smtplib


def send_email(subject, body, sender, recipient, smtp_server, smtp_port, smtp_user, smtp_password):
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart
    import smtplib

    msg = MIMEMultipart()
    msg["Subject"] = subject
    msg["From"] = sender
    msg["To"] = ", ".join(recipient) if isinstance(
        recipient, list) else recipient

    msg.attach(MIMEText(body, "plain"))

    with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
        server.login(smtp_user, smtp_password)
        server.sendmail(sender, recipient, msg.as_string())


def send_telegram_message(message: str):
    url = f"https://api.telegram.org/bot{TELEGRAM_CONFIG['bot_token']}/sendMessage"
    data = {
        "chat_id": TELEGRAM_CONFIG["chat_id"],
        "text": message
    }
    try:
        response = requests.post(url, data=data)
        response.raise_for_status()
    except Exception as e:
        print(f"텔레그램 전송 실패: {e}")
