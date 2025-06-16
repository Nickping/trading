import requests
import json
from env.update import refresh_token
from env.secrets import TOKEN


def request_with_logging(url, method="GET", headers=None, params=None, body=None):
    global TOKEN

    # 첫 요청
    res = make_request(url, method, headers, params, body)
    print(f"📡 요청 URL: {res.request.url}")
    print(
        f"📨 요청 헤더: {json.dumps(dict(res.request.headers), indent=2, ensure_ascii=False)}")
    if body:
        print(f"📝 요청 바디: {json.dumps(body, indent=2, ensure_ascii=False)}")
    print(f"📬 응답 코드: {res.status_code}")
    # print(
    #     f"📦 응답 내용: {json.dumps(res.json(), indent=2, ensure_ascii=False)}")

    # 500 에러 시 토큰 재발급 후 한 번 재시도
    if res.status_code == 500:
        print("⚠️ 500 오류 발생 → 토큰 갱신 시도")
        token = refresh_token()
        print(f"신규 발급 토큰 : {token}")
        if headers and "authorization" in headers:
            headers["authorization"] = token
        res = make_request(url, method, headers, params, body)
        print(f"📡 재요청 URL: {res.request.url}")
        print(f"📬 재요청 응답 코드: {res.status_code}")
        # print(
        #     f"📦 응답 내용: {json.dumps(res.json(), indent=2, ensure_ascii=False)}")

    try:
        return res.json()
    except Exception as e:
        print(f"❗ 응답 파싱 실패: {str(e)}")
        return {}


def make_request(url, method="GET", headers=None, params=None, body=None):
    if method == "GET":
        return requests.get(url, headers=headers, params=params, verify=False)
    elif method == "POST":
        return requests.post(url, headers=headers, json=body, params=params, verify=False)
    else:
        raise ValueError("지원하지 않는 HTTP 메서드입니다.")
