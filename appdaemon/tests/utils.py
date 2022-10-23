from datetime import datetime


def formatted_now():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
