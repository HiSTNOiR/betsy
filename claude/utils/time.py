import datetime
from datetime import datetime, timedelta, timezone
from typing import Optional, Tuple, Union, List


def get_utc_now() -> datetime:
    return datetime.now(timezone.utc)


def to_utc(dt: datetime) -> datetime:
    if dt.tzinfo is None:
        dt = dt.astimezone()
    return dt.astimezone(timezone.utc)


def format_datetime(
    dt: datetime,
    format_str: str = "%Y-%m-%d %H:%M:%S",
    include_timezone: bool = False
) -> str:
    if include_timezone and not format_str.endswith("%z"):
        format_str += " %z"
    return dt.strftime(format_str)


def parse_datetime(
    dt_str: str,
    format_str: str = "%Y-%m-%d %H:%M:%S",
    default_timezone: Optional[timezone] = None
) -> datetime:
    dt = datetime.strptime(dt_str, format_str)
    if dt.tzinfo is None and default_timezone is not None:
        dt = dt.replace(tzinfo=default_timezone)
    return dt


def format_duration(
    seconds: Union[int, float],
    include_seconds: bool = True,
    include_milliseconds: bool = False
) -> str:
    if seconds < 0:
        return "0s"
    days, remainder = divmod(seconds, 86400)
    hours, remainder = divmod(remainder, 3600)
    minutes, remainder = divmod(remainder, 60)
    seconds, milliseconds = divmod(remainder, 1)
    milliseconds = int(milliseconds * 1000)
    parts = []
    if days > 0:
        parts.append(f"{int(days)}d")
    if hours > 0 or days > 0:
        parts.append(f"{int(hours)}h")
    if minutes > 0 or hours > 0 or days > 0:
        parts.append(f"{int(minutes)}m")
    if include_seconds and (seconds > 0 or milliseconds > 0 or not parts):
        if include_milliseconds and milliseconds > 0:
            parts.append(f"{int(seconds)}.{milliseconds:03d}s")
        else:
            parts.append(f"{int(seconds)}s")
    return " ".join(parts)


def parse_duration(duration_str: str) -> float:
    import re
    if not duration_str or not isinstance(duration_str, str):
        raise ValueError(f"Invalid duration string: {duration_str}")
    pattern = r'(\d+\.?\d*)([dhms])'
    matches = re.findall(pattern, duration_str.lower())
    if not matches:
        raise ValueError(f"Invalid duration string: {duration_str}")
    total_seconds = 0.0
    for value, unit in matches:
        try:
            value = float(value)
        except ValueError:
            raise ValueError(f"Invalid numeric value in duration: {value}")

        if unit == 'd':
            total_seconds += value * 86400
        elif unit == 'h':
            total_seconds += value * 3600
        elif unit == 'm':
            total_seconds += value * 60
        elif unit == 's':
            total_seconds += value
    return total_seconds


def time_until(dt: datetime) -> timedelta:
    now = get_utc_now()
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return max(dt - now, timedelta(0))


def time_since(dt: datetime) -> timedelta:
    now = get_utc_now()
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return max(now - dt, timedelta(0))


def format_relative_time(dt: datetime, include_seconds: bool = True) -> str:
    now = get_utc_now()
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    if dt > now:
        delta = dt - now
        return f"in {format_duration(delta.total_seconds(), include_seconds)}"
    else:
        delta = now - dt
        return f"{format_duration(delta.total_seconds(), include_seconds)} ago"


def is_same_day(dt1: datetime, dt2: datetime) -> bool:
    if dt1.tzinfo is None:
        dt1 = dt1.replace(tzinfo=timezone.utc)
    if dt2.tzinfo is None:
        dt2 = dt2.replace(tzinfo=timezone.utc)
    dt1_utc = dt1.astimezone(timezone.utc)
    dt2_utc = dt2.astimezone(timezone.utc)
    return (dt1_utc.year == dt2_utc.year and
            dt1_utc.month == dt2_utc.month and
            dt1_utc.day == dt2_utc.day)


def add_time(
    dt: datetime,
    days: int = 0,
    hours: int = 0,
    minutes: int = 0,
    seconds: int = 0
) -> datetime:
    delta = timedelta(days=days, hours=hours, minutes=minutes, seconds=seconds)
    return dt + delta


def format_timestamp(dt: datetime) -> str:
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return str(int(dt.timestamp()))


def get_date_range(
    start_date: datetime,
    end_date: datetime,
    include_end: bool = True
) -> List[datetime]:
    if start_date > end_date:
        return []
    dates = []
    current_date = start_date.replace(
        hour=0, minute=0, second=0, microsecond=0)
    end = end_date.replace(hour=0, minute=0, second=0, microsecond=0)
    if include_end:
        end = add_time(end, days=1)
    while current_date < end:
        dates.append(current_date)
        current_date = add_time(current_date, days=1)
    return dates
