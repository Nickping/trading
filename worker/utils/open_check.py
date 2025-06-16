from datetime import datetime, time


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
