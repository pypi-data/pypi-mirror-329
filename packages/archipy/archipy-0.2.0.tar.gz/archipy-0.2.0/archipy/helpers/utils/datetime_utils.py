import time
from datetime import UTC, date, datetime, timedelta, timezone
from typing import ClassVar, Generator

import jdatetime
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from archipy.configs.base_config import BaseConfig


class DatetimeUtils:
    _holiday_cache: ClassVar[dict[str, tuple[bool, datetime]]] = {}

    @staticmethod
    def convert_to_jalali(target_date: date) -> jdatetime.date:
        """Convert a Gregorian date to a Jalali date."""
        return jdatetime.date.fromgregorian(date=target_date)

    @classmethod
    def is_holiday_in_iran(cls, target_date: date) -> bool:
        """
        Determine if the target date is a holiday in Iran, leveraging caching and API.
        """
        # Convert to Jalali date first
        jalali_date = cls.convert_to_jalali(target_date)
        date_str = target_date.strftime("%Y-%m-%d")
        current_time = datetime.now()

        # Check cache first
        is_cached, is_holiday = cls._check_cache(date_str, current_time)
        if is_cached:
            return is_holiday

        # Fetch holiday status and cache it
        is_holiday = cls._fetch_and_cache_holiday_status(jalali_date, date_str, current_time)
        return is_holiday

    @classmethod
    def _check_cache(cls, date_str: str, current_time: datetime) -> tuple[bool, bool]:
        """
        Check the cached data to avoid redundant API calls.
        """
        cached_data = cls._holiday_cache.get(date_str)
        if cached_data:
            is_holiday, expiry_time = cached_data
            if current_time < expiry_time:
                return True, is_holiday

            # Remove expired cache entry
            del cls._holiday_cache[date_str]

        return False, False

    @classmethod
    def _fetch_and_cache_holiday_status(
        cls,
        jalali_date: jdatetime.date,
        date_str: str,
        current_time: datetime,
    ) -> bool:
        """
        Fetch holiday status from the API and cache the result.
        """
        try:
            response = cls._call_holiday_api(jalali_date)
            is_holiday = cls._parse_holiday_response(response, jalali_date)

            # Cache the result with expiration
            expiry_time = current_time + timedelta(seconds=BaseConfig.global_config().DATETIME.CACHE_TTL)
            cls._holiday_cache[date_str] = (is_holiday, expiry_time)

            return is_holiday
        except requests.RequestException as e:
            print(f"Failed to check holiday status due to a network issue: {e}")
            return False

    @staticmethod
    def _call_holiday_api(jalali_date: jdatetime.date) -> dict:
        """
        Call the Time.ir API to fetch holiday data for the given Jalali date.
        """
        retry_strategy = Retry(
            total=BaseConfig.global_config().DATETIME.MAX_RETRIES,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["HEAD", "GET", "OPTIONS"],
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        session = requests.Session()
        session.mount("https://", adapter)

        url = DatetimeUtils._build_api_url(jalali_date)
        headers = {'x-api-key': BaseConfig.global_config().DATETIME.TIME_IR_API_KEY}
        response = session.get(url, headers=headers, timeout=BaseConfig.global_config().DATETIME.REQUEST_TIMEOUT)
        response.raise_for_status()
        return response.json()

    @staticmethod
    def _build_api_url(jalali_date: jdatetime.date) -> str:
        """
        Build the API URL with Jalali date parameters.
        """
        base_url = BaseConfig.global_config().DATETIME.TIME_IR_API_ENDPOINT
        return f"{base_url}?year={jalali_date.year}&month={jalali_date.month}&day={jalali_date.day}"

    @staticmethod
    def _parse_holiday_response(response_data: dict, jalali_date: jdatetime.date) -> bool:
        """
        Parse the API response to extract and return the holiday status.
        """
        event_list = response_data.get("data", {}).get("event_list", [])
        for event_info in event_list:
            if (
                event_info.get("jalali_year") == jalali_date.year
                and event_info.get("jalali_month") == jalali_date.month
                and event_info.get("jalali_day") == jalali_date.day
            ):
                return event_info.get("is_holiday", False)
        return False

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


if __name__ == '__main__':
    BaseConfig.set_global(BaseConfig())
    print(DatetimeUtils.is_holiday_in_iran(datetime(year=2025, month=3, day=19)))
    print(DatetimeUtils.is_holiday_in_iran(datetime(year=2025, month=3, day=19)))
    print(DatetimeUtils.is_holiday_in_iran(datetime(year=2025, month=3, day=19)))
