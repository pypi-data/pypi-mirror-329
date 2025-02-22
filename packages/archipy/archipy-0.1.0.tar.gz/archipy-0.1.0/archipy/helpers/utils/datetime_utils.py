import time
from datetime import UTC, datetime, timedelta, timezone
from typing import Generator


class DatetimeUtils:

    @classmethod
    def ensure_timezone_aware(cls, dt: datetime) -> datetime:
        """Ensure datetime is timezone-aware, converting if necessary."""
        if dt.tzinfo is None:
            return dt.replace(tzinfo=timezone.utc)
        return dt

    @classmethod
    def daterange(cls, start_date: datetime, end_date: datetime) -> Generator[datetime.date, None, None]:
        """Generate a range of dates from start_date to end_date, exclusive of end_date."""
        for n in range((end_date - start_date).days):
            yield (start_date + timedelta(n)).date()

    @classmethod
    def get_string_datetime_from_datetime(cls, dt: datetime, format_: str | None = None) -> str:
        """Convert a datetime object to a formatted string. Default format is ISO 8601."""
        format_ = format_ or "%Y-%m-%dT%H:%M:%S.%f"
        return dt.strftime(format_)

    @classmethod
    def standardize_string_datetime(cls, date_string: str) -> str:
        """Standardize a datetime string to the default format."""
        datetime_ = cls.get_datetime_from_string_datetime(date_string)
        return cls.get_string_datetime_from_datetime(datetime_)

    @classmethod
    def get_datetime_from_string_datetime(cls, date_string: str, format_: str | None = None) -> datetime:
        """Parse a string to a datetime object using given format, or ISO 8601 by default."""
        if format_ is None:
            return datetime.fromisoformat(date_string)
        return datetime.strptime(date_string, format_)

    @classmethod
    def get_string_datetime_now(cls) -> str:
        """Get the current datetime as a formatted string. Default format is ISO 8601."""
        return cls.get_string_datetime_from_datetime(cls.get_datetime_now())

    @classmethod
    def get_datetime_now(cls) -> datetime:
        """Get the current local datetime."""
        return datetime.now()

    @classmethod
    def get_datetime_utc_now(cls) -> datetime:
        """Get the current UTC datetime."""
        return datetime.now(UTC)

    @classmethod
    def get_epoch_time_now(cls) -> int:
        """Get the current time in seconds since the epoch."""
        return int(time.time())

    @classmethod
    def get_datetime_before_given_datetime_or_now(
        cls,
        weeks: int = 0,
        days: int = 0,
        hours: int = 0,
        minutes: int = 0,
        seconds: int = 0,
        datetime_given: datetime | None = None,
    ) -> datetime:
        """Subtract time from a given datetime or current datetime if not specified."""
        datetime_given = datetime_given or cls.get_datetime_now()
        return datetime_given - timedelta(weeks=weeks, days=days, hours=hours, minutes=minutes, seconds=seconds)

    @classmethod
    def get_datetime_after_given_datetime_or_now(
        cls,
        weeks: int = 0,
        days: int = 0,
        hours: int = 0,
        minutes: int = 0,
        seconds: int = 0,
        datetime_given: datetime | None = None,
    ) -> datetime:
        """Add time to a given datetime or current datetime if not specified."""
        datetime_given = datetime_given or cls.get_datetime_now()
        return datetime_given + timedelta(weeks=weeks, days=days, hours=hours, minutes=minutes, seconds=seconds)
