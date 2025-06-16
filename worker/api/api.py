from env.load_local import load_domestic_stocks, load_foreign_stocks
from utils.utils import is_domestic_open, is_foreign_open, filter_today_and_yesterday, filter_last_n_days
from datetime import datetime, timedelta
from analyze.analyze_domestic import analyze_domestic_stock_for_closed, analyze_domestic_stock_for_opened
from analyze.analyze_foreign import analyze_foreign_stock_for_closed, analyze_foreign_stock_for_opened, analyze_foreign_stock_for_opened_within_60min_RSI


def runDomestic():
    DOMESTIC_STOCKS = load_domestic_stocks()
    result = []
    today = datetime.now().strftime("%Y-%m-%d")
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    is_dom_open = is_domestic_open()    

    for stock in DOMESTIC_STOCKS:
        if is_dom_open:
            result.append(analyze_domestic_stock_for_opened(
                stock["name"], stock["symbol"]))
        else:
            result.append(analyze_domestic_stock_for_closed(
                stock["name"], stock["symbol"]))
    
    highlited = filter_today_and_yesterday(result, timestamp)    
    past_5days_buy = filter_last_n_days(result, timestamp, 5, "buy")
    past_5days_sell = filter_last_n_days(result, timestamp, 5, "sell")
    return {
        "records": result,        # 전체 결과 리스트
        "highlighted": highlited,  # 오늘/어제만 필터링한 리스트
        "past_5days_buy": past_5days_buy, # 지난 5일 매수 
        "past_5days_sell": past_5days_sell # 지난 5일 매도
    }

def runForeign():
    FOREIGN_STOCKS = load_foreign_stocks()
    result = []

    today = datetime.now().strftime("%Y-%m-%d")
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")    
    is_for_open = is_foreign_open()
    
    for stock in FOREIGN_STOCKS:
        if is_for_open:
            result.append(analyze_foreign_stock_for_opened_within_60min_RSI(
                stock["name"], stock["symbol"], stock["excd"]))
        else:
            result.append(analyze_foreign_stock_for_closed(
                stock["name"], stock["symbol"]))
        
    highlited = filter_today_and_yesterday(result, timestamp)
    past_5days_buy = filter_last_n_days(result, timestamp, 5, "buy")
    past_5days_sell = filter_last_n_days(result, timestamp, 5, "sell")
    return {
        "records": result,        # 전체 결과 리스트
        "highlighted": highlited,  # 오늘/어제만 필터링한 리스트
        "past_5days_buy": past_5days_buy, # 지난 5일 매수 
        "past_5days_sell": past_5days_sell # 지난 5일 매도
    }