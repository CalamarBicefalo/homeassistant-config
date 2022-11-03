from datetime import datetime, timedelta


def formatted_now() -> str:
    return format_date(datetime.now())


def formatted_yesterday() -> str:
    return format_date((datetime.now() - timedelta(days=1)))


def formatted_days_ago(days: int) -> str:
    return format_date((datetime.now() - timedelta(days=days)))


def formatted_minutes_ago(minutes: int) -> str:
    return format_date((datetime.now() - timedelta(minutes=minutes)))


def format_date(d) -> str:
    return d.strftime("%Y-%m-%d %H:%M:%S")


async def awaitable(thing):
    return thing
