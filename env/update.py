import requests
from env.secrets import APP_KEY, APP_SECRET
from env.endpoints import BASE_URL


def refresh_token():
    global TOKEN
    url = BASE_URL
    body = {
        "grant_type": "client_credentials",
        "appkey": APP_KEY,
        "appsecret": APP_SECRET
    }
    headers = {"content-type": "application/json"}

    try:
        res = requests.post(url, json=body, headers=headers, verify=False)
        if res.status_code == 200:
            TOKEN = "Bearer " + res.json().get("access_token", "")
            print("🔑 액세스 토큰 갱신 완료")
        else:
            print(f"❗ 토큰 갱신 실패: {res.text}")
    except Exception as e:
        print(f"❗ 토큰 갱신 예외: {str(e)}")
