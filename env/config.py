from datetime import datetime
from env.secrets import TOKEN, APP_SECRET, APP_KEY

DOMESTIC_STOCKS = {
    "삼성전자": "005930",
    "카카오뱅크": "323410",
    "네이버": "035420",
    "카카오": "035720",
    "SK이노베이션": "096770",
    "SK텔레콤": "017670",
    "SK하이닉스": "000660",
    "삼성전자(우)": "005935",
    "두산에너빌러티": "034020",
    "삼성중공업": "010140",
    "현대차": "005380"
}

FOREIGN_STOCKS = [
    {"name": "테슬라", "symbol": "TSLA"},
    {"name": "엔비디아", "symbol": "NVDA"},
    {"name": "QQQ", "symbol": "QQQ"},
    {"name": "SPY", "symbol": "SPY"},
    {"name": "팔란티어", "symbol": "PLTR"},
    {"name": "애플", "symbol": "AAPL"},
    {"name": "알파벳A", "symbol": "GOOGL"},
    {"name": "코카콜라", "symbol": "KO"},
    {"name": "마이크로소프트", "symbol": "MSFT"},
    {"name": "메타", "symbol": "META"},
    {"name": "월마트", "symbol": "WMT"},
    {"name": "엑슨모빌", "symbol": "XOM"}
]


def get_domestic_params(code: str, start_date="20240101"):
    return {
        "fid_cond_mrkt_div_code": "J",
        "fid_input_iscd": code,
        "fid_input_date_1": start_date,
        "fid_input_date_2": datetime.now().strftime("%Y%m%d"),
        "fid_period_div_code": "D",
        "fid_org_adj_prc": "1",
        "fid_etc_cls_code": ""
    }


def get_foreign_params(symbol: str, start_date="20240101"):
    return {
        "FID_COND_MRKT_DIV_CODE": "N",
        "FID_INPUT_ISCD": symbol,
        "FID_INPUT_DATE_1": start_date,
        "FID_INPUT_DATE_2": datetime.now().strftime("%Y%m%d"),
        "FID_PERIOD_DIV_CODE": "D"
    }


def get_default_headers():
    return {
        "authorization": TOKEN,
        "appkey": APP_KEY,
        "appsecret": APP_SECRET
    }
