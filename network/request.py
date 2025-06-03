import requests
import json


def request_api(method: str, url: str, headers: dict = None, params: dict = None, body: dict = None):
    try:
        if method.upper() == "GET":
            response = requests.get(
                url, headers=headers, params=params, verify=False)
        elif method.upper() == "POST":
            response = requests.post(
                url, headers=headers, json=body, params=params, verify=False)
        elif method.upper() == "PUT":
            response = requests.put(
                url, headers=headers, json=body, params=params, verify=False)
        elif method.upper() == "DELETE":
            response = requests.delete(
                url, headers=headers, json=body, params=params, verify=False)
        else:
            raise ValueError(f"지원하지 않는 HTTP 메서드입니다: {method}")

        print(f"📡 요청 URL: {response.request.url}")
        print(
            f"📨 요청 헤더: {json.dumps(dict(response.request.headers), indent=2, ensure_ascii=False)}")
        if body:
            print(f"📝 요청 바디: {json.dumps(body, indent=2, ensure_ascii=False)}")
        print(f"📬 응답 코드: {response.status_code}")
        # print(
        #     f"📦 응답 내용: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")

        return response
    except Exception as e:
        print(f"❗ 네트워크 요청 실패: {str(e)}")
        return None


def request_with_logging(url, method="GET", headers=None, params=None, body=None):
    try:
        if method == "GET":
            res = requests.get(url, headers=headers,
                               params=params, verify=False)
        elif method == "POST":
            res = requests.post(url, headers=headers,
                                json=body, params=params, verify=False)
        else:
            raise ValueError("지원하지 않는 HTTP 메서드입니다.")

        print(f"📡 요청 URL: {res.request.url}")
        print(
            f"📨 요청 헤더: {json.dumps(dict(res.request.headers), indent=2, ensure_ascii=False)}")
        if body:
            print(f"📝 요청 바디: {json.dumps(body, indent=2, ensure_ascii=False)}")
        print(f"📬 응답 코드: {res.status_code}")
        # print(
        #     f"📦 응답 내용: {json.dumps(res.json(), indent=2, ensure_ascii=False)}")

        return res.json()
    except Exception as e:
        print(f"❗ 요청 실패: {str(e)}")
        return {}
