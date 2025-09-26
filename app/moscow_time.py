from datetime import datetime
import pytz


def moscow_time():
    moscow_tz = pytz.timezone("Europe/Moscow")
    now = datetime.now(moscow_tz)
    return now.replace(microsecond=0, tzinfo=None)
