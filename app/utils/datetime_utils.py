from datetime import datetime
from zoneinfo import ZoneInfo


MEXICO_TZ = ZoneInfo("America/Mexico_City")


def now_mexico() -> datetime:
    """Regresa datetime actual en zona México"""
    return datetime.now(MEXICO_TZ)


def format_mexico(dt: datetime) -> str:
    """Convierte datetime a formato DD-MM-YY HH:MM:SS"""
    if not dt:
        return None
    return dt.astimezone(MEXICO_TZ).strftime("%d-%m-%y %H:%M:%S")