from datetime import datetime, timedelta
from env.config import DOMESTIC_STOCKS, FOREIGN_STOCKS
from network.broadcast import send_email
from network.broadcast import send_telegram_message
from env.secrets import EMAIL_CONFIG
from api.api import runForeign, runDomestic
from flask import Flask, request, jsonify
import re
import schedule
import time
import re

app = Flask(__name__)


# def main():
#     domestic = runDomestic()
#     foreign = runForeign()    

@app.route("/run_domestic", methods=["POST"])
def run_domestic():
    data = request.json or {}
    is_open = data.get("is_open", False)  # 기본값: 장외
    result = runDomestic(is_open=is_open)
    return jsonify({"result": result})

@app.route("/run_foreign", methods=["POST"])
def run_foreign():
    data = request.json or {}
    is_open = data.get("is_open", False)  # 기본값: 장외
    result = runForeign(is_open=is_open)
    return jsonify({"result": result})


if __name__ == "__main__":
    app.run(port=7777)

# # 최초 실행
# main()

# # 60분마다 반복
# schedule.every(60).minutes.do(main)

# # 루프 실행
# while True:
#     schedule.run_pending()
#     time.sleep(10)
