from datetime import datetime, date
from zoneinfo import ZoneInfo

TIME_ZONE = ZoneInfo("America/Chicago")

def convert_dt(s: str) -> datetime:
    utc_dt = datetime.fromisoformat(s.replace("Z", "+00:00"))

    return utc_dt.astimezone(TIME_ZONE)

def format_dt(s: str, format_str: str) -> str:
    """
    Converts a string timestamp to 'America/Chicago' time zone and formats in the specified format.
    """
    return convert_dt(s).strftime(format_str)


def display_games_dt(d1: str, d2: str) -> str:
    formatted_d1 = format_dt(d1, "%m/%d/%Y")
    formatted_d2 = format_dt(d2, "%m/%d/%Y")
    today = datetime.now(TIME_ZONE).strftime("%m/%d/%Y")
    
    if formatted_d1 == formatted_d2 == today:
        return "Today"
    elif formatted_d1 == formatted_d2:
        return f"on {formatted_d1}"
    else:
        return f"from {formatted_d1} - {formatted_d2}"