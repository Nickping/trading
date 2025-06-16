BASE_URL = "https://openapi.koreainvestment.com:9443"

DOMESTIC_DAILY_ENDPOINT = BASE_URL + \
    "/uapi/domestic-stock/v1/quotations/inquire-daily-itemchartprice"
FOREIGN_DAILY_ENDPOINT = BASE_URL + \
    "/uapi/overseas-price/v1/quotations/inquire-daily-chartprice"

FOREIGN_TIME_ITEM_CHART_PRICE = BASE_URL + \
    "/uapi/overseas-price/v1/quotations/inquire-time-itemchartprice"

ACCESS_TOKEN_UPDATE = BASE_URL + \
    "/oauth2/tokenP"
