import requests
from env.secrets import APP_KEY, APP_SECRET, set_token, get_token
from env.endpoints import ACCESS_TOKEN_UPDATE
import json


def refresh_token():
    url = ACCESS_TOKEN_UPDATE
    body = {
        "grant_type": "client_credentials",
        "appkey": APP_KEY,
        "appsecret": APP_SECRET
    }
    headers = {"content-type": "application/json"}

    try:
        res = requests.post(url, json=body, headers=headers, verify=False)
        if res.status_code == 200:
            set_token("Bearer " + res.json().get("access_token", ""))
            print("🔑 액세스 토큰 갱신 완료")
            return get_token()
        else:
            print(f"❗ 토큰 갱신 실패: {res.text}")
            print(
                f"📦 응답 내용: {json.dumps(res.json(), indent=2, ensure_ascii=False)}")
    except Exception as e:
        print(f"❗ 토큰 갱신 예외: {str(e)}")
        return None
