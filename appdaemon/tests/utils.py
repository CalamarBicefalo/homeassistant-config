from datetime import datetime, timedelta


def formatted_now():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def formatted_yesterday():
    return (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S")
