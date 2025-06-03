
# 📁 app/send_email.py

from email.mime.text import MIMEText
from email.header import Header
import smtplib


def send_email(subject, body, sender, recipient, smtp_server, smtp_port, smtp_user, smtp_password):
    msg = MIMEText(body, "plain", "utf-8")
    msg['Subject'] = Header(subject, "utf-8")
    msg['From'] = sender
    msg['To'] = recipient

    with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
        server.login(smtp_user, smtp_password)
        server.sendmail(sender, recipient, msg.as_string())
