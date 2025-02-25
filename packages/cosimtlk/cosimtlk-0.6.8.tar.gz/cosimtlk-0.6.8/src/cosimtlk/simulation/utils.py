import functools
from datetime import timedelta
from zoneinfo import ZoneInfo

import cron_converter

from cosimtlk.models import DateTimeLike

UTC = ZoneInfo("UTC")


def ensure_tz(dt: DateTimeLike, default_tz: ZoneInfo = UTC) -> DateTimeLike:
    """Add timezone information to a datetime object if missing.

    Args:
        dt: Datetime object with or without timezone information.
        default_tz: Timezone information to add in case the datetime object has no timezone info.
    """
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=default_tz)
    return dt


def every(*, seconds: int = 0, minutes: int = 0, hours: int = 0, days: int = 0):
    """Decorator to schedule a process to run forever with a given delay."""
    total_delay_seconds = seconds + minutes * 60 + hours * 3600 + days * 86400
    if total_delay_seconds <= 0:
        msg = "At least one time unit must be specified."
        raise ValueError(msg)

    def decorator(func):
        """Decorator to schedule a process to run forever with a given delay."""

        @functools.wraps(func)
        def wrapped(self, *args, **kwargs):
            """Wrapper to schedule a process to run forever with a given delay."""
            while True:
                func(self, *args, **kwargs)
                yield self.ctx.env.timeout(total_delay_seconds)

        return wrapped

    return decorator


def cron(*, minute="*", hour="*", day="*", month="*", weekday="*"):
    """Decorator to schedule a process to run forever with a given cron expression."""
    cron_str = " ".join([minute.strip(), hour.strip(), day.strip(), month.strip(), weekday.strip()])
    cron_instance = cron_converter.Cron(cron_str)

    def decorator(func):
        @functools.wraps(func)
        def wrapper(self, *args, **kwargs):
            # To return the simulation time as first date if exact match
            last_run = self.ctx.current_datetime
            schedule = cron_instance.schedule(last_run - timedelta(seconds=1))
            while True:
                next_run = schedule.next()
                next_in_seconds = int((next_run - last_run).total_seconds())
                yield self.ctx.env.timeout(next_in_seconds)
                func(self, *args, **kwargs)
                last_run = next_run

        return wrapper

    return decorator


def namespaced(*parts: str, separator: str = ".") -> str:
    """Join parts with a separator to create a namespaced string."""
    return separator.join(parts)
