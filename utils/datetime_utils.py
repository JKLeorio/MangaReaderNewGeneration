from datetime import datetime, timezone

def get_current_time() -> datetime:
    """
    returns the current time in utc timezone
    """
    return datetime.now(tz=timezone.utc)
