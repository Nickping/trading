import requests


EMAIL_CONFIG = {
    "sender": "dordong327@gmail.com",
    # 📬 수신자 리스트로 변경
    # "recipient": ["dordong327@gmail.com", "jbk7544@naver.com"],
    "recipient": ["dordong327@gmail.com"],
    "smtp_server": "smtp.gmail.com",
    "smtp_port": 465,
    "smtp_user": "dordong327@gmail.com",
    "smtp_password": "doxcryfintvhcvxh"
}


TELEGRAM_CONFIG = {
    "bot_token": "7883583558:AAGYb-p368Evjp0Mj8jVlM8pmUxiiBzGTfI",
    "chat_id": "7085263126"
}


APP_KEY = "PSlcp3lgMB9k27Q3aqbtHJB0wNMMCvoJt586"
APP_SECRET = "9ywyyHyo466aAguNMWf9s4M7V/qLXuo05AFXmK7aaHnXCWDF2lCTc25W12dxTVS2ZnROuZgFwp/0kz7EAftXBvZokSXrb2+t4RJHd6Vw+2Sx2Nu+zXIegAB6Em1SrDpt48oRwygsNKWJRlBPyjEM7vhEf/xyepK62MphEPCAulGSO4lVIkM="
TOKEN = "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJzdWIiOiJ0b2tlbiIsImF1ZCI6ImIxOGQ4NWQ5LTdkMjQtNDZmNS1hYjJkLTlmODJkODZjNTBmOSIsInByZHRfY2QiOiIiLCJpc3MiOiJ1bm9ndyIsImV4cCI6MTc1MDE3Mjc2NSwiaWF0IjoxNzUwMDg2MzY1LCJqdGkiOiJQU2xjcDNsZ01COWsyN1EzYXFidEhKQjB3Tk1NQ3ZvSnQ1ODYifQ.xggmeRa9t9pVEeDaOWMzsgh200Dkiy2gyAllRhoB2RTx1KDokjrhOBE8o6ZES6l8J0MUYvGFH-yaS77rREaJ1A"


def set_token(value):
    global TOKEN
    TOKEN = value


def get_token():
    return TOKEN
