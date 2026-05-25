from datetime import datetime
from zoneinfo import ZoneInfo

def convert_dt(s: str) -> datetime:
    utc_dt = datetime.fromisoformat(s.replace("Z", "+00:00"))

    return utc_dt.astimezone(ZoneInfo("America/Chicago"))
