from datetime import datetime, time, timedelta, date
import re

def is_foreign_open() -> bool:
    now = datetime.utcnow()  # 미국장은 UTC 기준으로 판단해야 정확함

    # 미국 동부 기준: 월~금, 09:30 ~ 16:00 → UTC 기준으론 14:30 ~ 21:00
    return (
        now.weekday() < 5 and
        time(14, 30) <= now.time() < time(21, 0)
    )


def is_domestic_open() -> bool:
    now = datetime.now()
    # 한국 시간 기준: 월~금, 09:00 ~ 15:30
    return (
        now.weekday() < 5 and  # 월~금
        time(9, 0) <= now.time() < time(15, 30)
    )

# def filter_today_and_yesterday(results_2d, today_str):    
#     today = datetime.strptime(today_str, "%Y-%m-%d %H:%M").date()
#     yesterday = today - timedelta(days=1)

#     flat_results = flatten_results(results_2d)    
#     filtered = []
#     for entry in flat_results:
#         date_str = entry.get("date")
#         if not date_str:
#             continue  # "date"가 없는 항목 건너뜀
#         try:
#             entry_date = datetime.strptime(date_str, "%Y-%m-%d %H:%M").date()
#             if entry_date in (today, yesterday):
#                 filtered.append(entry)
#         except Exception as e:
#             print(f"❌ 날짜 파싱 실패: {entry['date']} - {e}")
#             continue

#     return filtered



def filter_today_and_yesterday(entries, now_str: str):
    """
    today와 yesterday 날짜에 해당하는 항목만 필터링하여 반환한다.
    entries: [{..., "date": "2025-06-16 13:00"}, ...]
    """
    try:
        now = datetime.strptime(now_str, "%Y-%m-%d %H:%M").date()
    except Exception as e:
        print(f"❌ 기준일 파싱 실패: {now_str} - {e}")
        return []

    yesterday = now - timedelta(days=1)
    flat_results = flatten_results(entries)    
    filtered = []

    for entry in flat_results:
        entry_date = parse_stock_date(entry.get("date"))
        
        if not isinstance(entry, dict):
            continue
        if not entry_date:
            continue  # "date"가 없는 항목 건너뜀
        
        if not entry_date:
            print(f"❌ 날짜 파싱 실패: {entry.get('date')}")
            continue

        if entry_date in (now, yesterday):
            filtered.append(entry)

    return filtered

def filter_last_n_days(entries, today_str, n, trade_type):
    try:
        today = datetime.strptime(today_str, "%Y-%m-%d %H:%M").date()
    except Exception as e:
        print(f"❌ 기준일 파싱 실패: {today_str} - {e}")
        return []
    
    
    earliest = today - timedelta(days=n)
    flat_results = flatten_results(entries)    
    filtered = []

    for entry in flat_results:
        if not isinstance(entry, dict):
            continue

        entry_date = parse_stock_date(entry.get("date"))
        if not entry_date:
            print(f"❌ 날짜 파싱 실패: {entry.get('date')}")
            continue

        if earliest <= entry_date <= today:
            if trade_type:
                if entry.get("type") == trade_type:
                    filtered.append(entry)
            else:
                filtered.append(entry)

    return filtered
        
    print(f"🕒 기준일: {today} | 검색기간: {earliest} ~ {today}")
    print(f"✅ {trade_type} 후보 개수: {len(filtered)}")


    return filtered



def flatten_results(nested_results):
    return [
        entry
        for group in nested_results
        if isinstance(group, list)
        for entry in group
        if isinstance(entry, dict)
    ]
    

def parse_stock_date(date_str: str) -> date:
    """
    주식 데이터 날짜 문자열을 datetime.date 객체로 변환한다.
    
    지원하는 포맷:
    - "20250616" → 국내 일봉 (YYYYMMDD)
    - "2025-06-16 13:00" → 장중 (YYYY-MM-DD HH:MM)
    - "2025-06-16" → 장마감 (YYYY-MM-DD)
    - datetime.date 객체가 이미 들어오면 그대로 반환

    예외 발생 시 None 반환
    """
    if isinstance(date_str, date):
        return date_str  # 이미 date 객체일 경우
    
    if not date_str:
        return None  # "date"가 없는 항목 건너뜀

    formats = ["%Y%m%d", "%Y-%m-%d", "%Y-%m-%d %H:%M"]
    
    for fmt in formats:
        try:
            return datetime.strptime(date_str, fmt).date()
        except ValueError:
            continue
    return None