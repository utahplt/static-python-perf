"""
Implementations of SQL functions for SQLite.
"""
import __static__

import functools
import random
import statistics
import zoneinfo
from datetime import timedelta
from hashlib import md5, sha1, sha224, sha256, sha384, sha512
from math import (
    acos,
    asin,
    atan,
    atan2,
    ceil,
    cos,
    degrees,
    exp,
    floor,
    fmod,
    log,
    pi,
    radians,
    sin,
    sqrt,
    tan,
)
from re import search as re_search

from django.db.backends.utils import (
    split_tzname_delta,
    typecast_time,
    typecast_timestamp,
)
from django.utils import timezone
from django.utils.duration import duration_microseconds

# for types
import sqlite3
from datetime import datetime, time, date
from typing import Optional, Union, Callable, Any

### SECTION SEPARATOR ###

def register(connection: sqlite3.Connection):
    create_deterministic_function: Callable[[str, int, Callable[..., Any]], None] = functools.partial(
        connection.create_function,
        deterministic=True,
    )
    create_deterministic_function("django_date_extract", 2, _sqlite_datetime_extract)
    create_deterministic_function("django_date_trunc", 4, _sqlite_date_trunc)
    create_deterministic_function(
        "django_datetime_cast_date", 3, _sqlite_datetime_cast_date
    )
    create_deterministic_function(
        "django_datetime_cast_time", 3, _sqlite_datetime_cast_time
    )
    create_deterministic_function(
        "django_datetime_extract", 4, _sqlite_datetime_extract
    )
    create_deterministic_function("django_datetime_trunc", 4, _sqlite_datetime_trunc)
    create_deterministic_function("django_time_extract", 2, _sqlite_time_extract)
    create_deterministic_function("django_time_trunc", 4, _sqlite_time_trunc)
    create_deterministic_function("django_time_diff", 2, _sqlite_time_diff)
    create_deterministic_function("django_timestamp_diff", 2, _sqlite_timestamp_diff)
    create_deterministic_function("django_format_dtdelta", 3, _sqlite_format_dtdelta)
    create_deterministic_function("regexp", 2, _sqlite_regexp)
    create_deterministic_function("BITXOR", 2, _sqlite_bitxor)
    create_deterministic_function("COT", 1, _sqlite_cot)
    create_deterministic_function("LPAD", 3, _sqlite_lpad)
    create_deterministic_function("MD5", 1, _sqlite_md5)
    create_deterministic_function("REPEAT", 2, _sqlite_repeat)
    create_deterministic_function("REVERSE", 1, _sqlite_reverse)
    create_deterministic_function("RPAD", 3, _sqlite_rpad)
    create_deterministic_function("SHA1", 1, _sqlite_sha1)
    create_deterministic_function("SHA224", 1, _sqlite_sha224)
    create_deterministic_function("SHA256", 1, _sqlite_sha256)
    create_deterministic_function("SHA384", 1, _sqlite_sha384)
    create_deterministic_function("SHA512", 1, _sqlite_sha512)
    create_deterministic_function("SIGN", 1, _sqlite_sign)
    # Don't use the built-in RANDOM() function because it returns a value
    # in the range [-1 * 2^63, 2^63 - 1] instead of [0, 1).
    connection.create_function("RAND", 0, random.random)
    connection.create_aggregate("STDDEV_POP", 1, StdDevPop)
    connection.create_aggregate("STDDEV_SAMP", 1, StdDevSamp)
    connection.create_aggregate("VAR_POP", 1, VarPop)
    connection.create_aggregate("VAR_SAMP", 1, VarSamp)
    # Some math functions are enabled by default in SQLite 3.35+.
    sql: str = "select sqlite_compileoption_used('ENABLE_MATH_FUNCTIONS')"
    if not connection.execute(sql).fetchone()[0]:
        create_deterministic_function("ACOS", 1, _sqlite_acos)
        create_deterministic_function("ASIN", 1, _sqlite_asin)
        create_deterministic_function("ATAN", 1, _sqlite_atan)
        create_deterministic_function("ATAN2", 2, _sqlite_atan2)
        create_deterministic_function("CEILING", 1, _sqlite_ceiling)
        create_deterministic_function("COS", 1, _sqlite_cos)
        create_deterministic_function("DEGREES", 1, _sqlite_degrees)
        create_deterministic_function("EXP", 1, _sqlite_exp)
        create_deterministic_function("FLOOR", 1, _sqlite_floor)
        create_deterministic_function("LN", 1, _sqlite_ln)
        create_deterministic_function("LOG", 2, _sqlite_log)
        create_deterministic_function("MOD", 2, _sqlite_mod)
        create_deterministic_function("PI", 0, _sqlite_pi)
        create_deterministic_function("POWER", 2, _sqlite_power)
        create_deterministic_function("RADIANS", 1, _sqlite_radians)
        create_deterministic_function("SIN", 1, _sqlite_sin)
        create_deterministic_function("SQRT", 1, _sqlite_sqrt)
        create_deterministic_function("TAN", 1, _sqlite_tan)

### SECTION SEPARATOR ###

def _sqlite_datetime_parse(dt: Optional[str], tzname: Optional[str] = None, conn_tzname: Optional[str] = None) -> Optional[datetime]:
    if dt is None:
        return None
    try:
        dt: datetime = typecast_timestamp(dt)
    except (TypeError, ValueError):
        return None
    if conn_tzname:
        dt: datetime = dt.replace(tzinfo=zoneinfo.ZoneInfo(conn_tzname))
    if tzname is not None and tzname != conn_tzname:
        tzname, sign, offset = split_tzname_delta(tzname)
        if offset:
            hours: str
            minutes: str
            hours, minutes = offset.split(":")
            offset_delta: timedelta = timedelta(hours=int(hours), minutes=int(minutes))
            dt += offset_delta if sign == "+" else -offset_delta
        # The tzname may originally be just the offset e.g. "+3:00",
        # which becomes an empty string after splitting the sign and offset.
        # In this case, use the conn_tzname as fallback.
        dt: datetime = timezone.localtime(dt, zoneinfo.ZoneInfo(tzname or conn_tzname))
    return dt

### SECTION SEPARATOR ###

def _sqlite_date_trunc(lookup_type: str, dt: Optional[str], tzname: Optional[str], conn_tzname: Optional[str]) -> Optional[str]:
    dt = _sqlite_datetime_parse(dt, tzname, conn_tzname)
    if dt is None:
        return None
    if lookup_type == "year":
        return f"{dt.year:04d}-01-01"
    elif lookup_type == "quarter":
        month_in_quarter: int = dt.month - (dt.month - 1) % 3
        return f"{dt.year:04d}-{month_in_quarter:02d}-01"
    elif lookup_type == "month":
        return f"{dt.year:04d}-{dt.month:02d}-01"
    elif lookup_type == "week":
        dt -= timedelta(days=dt.weekday())
        return f"{dt.year:04d}-{dt.month:02d}-{dt.day:02d}"
    elif lookup_type == "day":
        return f"{dt.year:04d}-{dt.month:02d}-{dt.day:02d}"
    raise ValueError(f"Unsupported lookup type: {lookup_type!r}")

### SECTION SEPARATOR ###

def _sqlite_time_trunc(lookup_type: str, dt: Optional[Union[str, time, datetime]], tzname: Optional[str], conn_tzname: Optional[str]) -> Optional[str]:
    if dt is None:
        return None
    dt_parsed: Optional[datetime] = _sqlite_datetime_parse(dt, tzname, conn_tzname)
    if dt_parsed is None:
        try:
            dt = typecast_time(dt)
        except (ValueError, TypeError):
            return None
    else:
        dt = dt_parsed
    if lookup_type == "hour":
        return f"{dt.hour:02d}:00:00"
    elif lookup_type == "minute":
        return f"{dt.hour:02d}:{dt.minute:02d}:00"
    elif lookup_type == "second":
        return f"{dt.hour:02d}:{dt.minute:02d}:{dt.second:02d}"
    raise ValueError(f"Unsupported lookup type: {lookup_type!r}")

### SECTION SEPARATOR ###

def _sqlite_datetime_cast_date(dt: Optional[Union[str, datetime]], tzname: Optional[str], conn_tzname: Optional[str]) -> Optional[str]:
    dt = _sqlite_datetime_parse(dt, tzname, conn_tzname)
    if dt is None:
        return None
    return dt.date().isoformat()

### SECTION SEPARATOR ###

def _sqlite_datetime_cast_time(dt: Optional[Union[str, datetime]], tzname: Optional[str], conn_tzname: Optional[str]) -> Optional[str]:
    dt = _sqlite_datetime_parse(dt, tzname, conn_tzname)
    if dt is None:
        return None
    return dt.time().isoformat()

### SECTION SEPARATOR ###

def _sqlite_datetime_extract(lookup_type: str, dt: Optional[Union[str, datetime]], tzname: Optional[str] = None, conn_tzname: Optional[str] = None) -> Optional[Union[int, str]]:
    dt = _sqlite_datetime_parse(dt, tzname, conn_tzname)
    if dt is None:
        return None
    if lookup_type == "week_day":
        return (dt.isoweekday() % 7) + 1
    elif lookup_type == "iso_week_day":
        return dt.isoweekday()
    elif lookup_type == "week":
        return dt.isocalendar().week
    elif lookup_type == "quarter":
        return ceil(dt.month / 3)
    elif lookup_type == "iso_year":
        return dt.isocalendar().year
    else:
        return getattr(dt, lookup_type)

### SECTION SEPARATOR ###

def _sqlite_datetime_trunc(lookup_type: str, dt: Optional[Union[str, datetime]], tzname: Optional[str], conn_tzname: Optional[str]) -> Optional[str]:
    dt = _sqlite_datetime_parse(dt, tzname, conn_tzname)
    if dt is None:
        return None
    if lookup_type == "year":
        return f"{dt.year:04d}-01-01 00:00:00"
    elif lookup_type == "quarter":
        month_in_quarter: int = dt.month - (dt.month - 1) % 3
        return f"{dt.year:04d}-{month_in_quarter:02d}-01 00:00:00"
    elif lookup_type == "month":
        return f"{dt.year:04d}-{dt.month:02d}-01 00:00:00"
    elif lookup_type == "week":
        dt -= timedelta(days=dt.weekday())
        return f"{dt.year:04d}-{dt.month:02d}-{dt.day:02d} 00:00:00"
    elif lookup_type == "day":
        return f"{dt.year:04d}-{dt.month:02d}-{dt.day:02d} 00:00:00"
    elif lookup_type == "hour":
        return f"{dt.year:04d}-{dt.month:02d}-{dt.day:02d} {dt.hour:02d}:00:00"
    elif lookup_type == "minute":
        return (
            f"{dt.year:04d}-{dt.month:02d}-{dt.day:02d} "
            f"{dt.hour:02d}:{dt.minute:02d}:00"
        )
    elif lookup_type == "second":
        return (
            f"{dt.year:04d}-{dt.month:02d}-{dt.day:02d} "
            f"{dt.hour:02d}:{dt.minute:02d}:{dt.second:02d}"
        )
    raise ValueError(f"Unsupported lookup type: {lookup_type!r}")

### SECTION SEPARATOR ###

def _sqlite_time_extract(lookup_type: str, dt: Optional[Union[str, time]]) -> Optional[Union[int, str]]:
    if dt is None:
        return None
    try:
        dt = typecast_time(dt)
    except (ValueError, TypeError):
        return None
    return getattr(dt, lookup_type)

### SECTION SEPARATOR ###

def _sqlite_prepare_dtdelta_param(conn: str, param: Union[int, str]) -> Union[timedelta, datetime]:
    if conn in ["+", "-"]:
        if isinstance(param, int):
            return timedelta(0, 0, param)
        else:
            return typecast_timestamp(param)
    return param

### SECTION SEPARATOR ###

def _sqlite_format_dtdelta(connector: Optional[str], lhs: Optional[Union[int, str]], rhs: Optional[Union[int, str]]) -> Optional[Union[str, float]]:
    """
    LHS and RHS can be either:
    - An integer number of microseconds
    - A string representing a datetime
    - A scalar value, e.g. float
    """
    if connector is None or lhs is None or rhs is None:
        return None
    connector = connector.strip()
    try:
        real_lhs: Union[timedelta, datetime] = _sqlite_prepare_dtdelta_param(connector, lhs)
        real_rhs: Union[timedelta, datetime] = _sqlite_prepare_dtdelta_param(connector, rhs)
    except (ValueError, TypeError):
        return None
    if connector == "+":
        # typecast_timestamp() returns a date or a datetime without timezone.
        # It will be formatted as "%Y-%m-%d" or "%Y-%m-%d %H:%M:%S[.%f]"
        out: str = str(real_lhs + real_rhs)
    elif connector == "-":
        out: str = str(real_lhs - real_rhs)
    elif connector == "*":
        out: str = real_lhs * real_rhs
    else:
        out: str = real_lhs / real_rhs
    return out

### SECTION SEPARATOR ###

def _sqlite_time_diff(lhs: Optional[str], rhs: Optional[str]) -> Optional[int]:
    if lhs is None or rhs is None:
        return None
    left: time = typecast_time(lhs)
    right: time = typecast_time(rhs)
    return (
        (left.hour * 60 * 60 * 1000000)
        + (left.minute * 60 * 1000000)
        + (left.second * 1000000)
        + (left.microsecond)
        - (right.hour * 60 * 60 * 1000000)
        - (right.minute * 60 * 1000000)
        - (right.second * 1000000)
        - (right.microsecond)
    )

### SECTION SEPARATOR ###

def _sqlite_timestamp_diff(lhs: Optional[str], rhs: Optional[str]) -> Optional[int]:
    if lhs is None or rhs is None:
        return None
    left: date = typecast_timestamp(lhs)
    right: date = typecast_timestamp(rhs)
    return duration_microseconds(left - right)

### SECTION SEPARATOR ###

def _sqlite_regexp(pattern: Optional[str], string: Optional[str]) -> Optional[bool]:
    if pattern is None or string is None:
        return None
    if not isinstance(string, str):
        string: str = str(string)
    return bool(re_search(pattern, string))

### SECTION SEPARATOR ###

def _sqlite_acos(x: Optional[float]) -> Optional[float]:
    if x is None:
        return None
    return acos(x)

### SECTION SEPARATOR ###

def _sqlite_asin(x: Optional[float]) -> Optional[float]:
    if x is None:
        return None
    return asin(x)

### SECTION SEPARATOR ###

def _sqlite_atan(x: Optional[float]) -> Optional[float]:
    if x is None:
        return None
    return atan(x)

### SECTION SEPARATOR ###

def _sqlite_atan2(y: Optional[float], x: Optional[float]) -> Optional[float]:
    if y is None or x is None:
        return None
    return atan2(y, x)

### SECTION SEPARATOR ###

def _sqlite_bitxor(x: Optional[int], y: Optional[int]) -> Optional[int]:
    if x is None or y is None:
        return None
    return x ^ y

### SECTION SEPARATOR ###

def _sqlite_ceiling(x: Optional[float]) -> Optional[int]:
    if x is None:
        return None
    return ceil(x)

### SECTION SEPARATOR ###

def _sqlite_cos(x: Optional[float]) -> Optional[float]:
    if x is None:
        return None
    return cos(x)

### SECTION SEPARATOR ###

def _sqlite_cot(x: Optional[float]) -> Optional[float]:
    if x is None:
        return None
    return 1 / tan(x)

### SECTION SEPARATOR ###

def _sqlite_degrees(x: Optional[float]) -> Optional[float]:
    if x is None:
        return None
    return degrees(x)

### SECTION SEPARATOR ###

def _sqlite_exp(x: Optional[float]) -> Optional[float]:
    if x is None:
        return None
    return exp(x)

### SECTION SEPARATOR ###

def _sqlite_floor(x: Optional[float]) -> Optional[int]:
    if x is None:
        return None
    return floor(x)

### SECTION SEPARATOR ###

def _sqlite_ln(x: Optional[float]) -> Optional[float]:
    if x is None:
        return None
    return log(x)

### SECTION SEPARATOR ###

def _sqlite_log(base: Optional[float], x: Optional[float]) -> Optional[float]:
    if base is None or x is None:
        return None
    # Arguments reversed to match SQL standard.
    return log(x, base)

### SECTION SEPARATOR ###

def _sqlite_lpad(text: Optional[str], length: Optional[int], fill_text: Optional[str]) -> Optional[str]:
    if text is None or length is None or fill_text is None:
        return None
    delta: int = length - len(text)
    if delta <= 0:
        return text[:length]
    return (fill_text * length)[:delta] + text

### SECTION SEPARATOR ###

def _sqlite_md5(text: Optional[str]) -> Optional[str]:
    if text is None:
        return None
    return md5(text.encode()).hexdigest()

### SECTION SEPARATOR ###

def _sqlite_mod(x: Optional[float], y: Optional[float]) -> Optional[float]:
    if x is None or y is None:
        return None
    return fmod(x, y)

### SECTION SEPARATOR ###

def _sqlite_pi() -> float:
    return pi

### SECTION SEPARATOR ###

def _sqlite_power(x: Optional[float], y: Optional[float]) -> Optional[float]:
    if x is None or y is None:
        return None
    return x**y

### SECTION SEPARATOR ###

def _sqlite_radians(x: Optional[float]) -> Optional[float]:
    if x is None:
        return None
    return radians(x)

### SECTION SEPARATOR ###

def _sqlite_repeat(text: Optional[str], count: Optional[int]) -> Optional[str]:
    if text is None or count is None:
        return None
    return text * count

### SECTION SEPARATOR ###

def _sqlite_reverse(text: Optional[str]) -> Optional[str]:
    if text is None:
        return None
    return text[::-1]

### SECTION SEPARATOR ###

def _sqlite_rpad(text: Optional[str], length: Optional[int], fill_text: Optional[str]) -> Optional[str]:
    if text is None or length is None or fill_text is None:
        return None
    return (text + fill_text * length)[:length]

### SECTION SEPARATOR ###

def _sqlite_sha1(text: Optional[str]) -> Optional[str]:
    if text is None:
        return None
    return sha1(text.encode()).hexdigest()

### SECTION SEPARATOR ###

def _sqlite_sha224(text: Optional[str]) -> Optional[str]:
    if text is None:
        return None
    return sha224(text.encode()).hexdigest()

### SECTION SEPARATOR ###

def _sqlite_sha256(text: Optional[str]) -> Optional[str]:
    if text is None:
        return None
    return sha256(text.encode()).hexdigest()

### SECTION SEPARATOR ###

def _sqlite_sha384(text: Optional[str]) -> Optional[str]:
    if text is None:
        return None
    return sha384(text.encode()).hexdigest()

### SECTION SEPARATOR ###

def _sqlite_sha512(text: Optional[str]) -> Optional[str]:
    if text is None:
        return None
    return sha512(text.encode()).hexdigest()

### SECTION SEPARATOR ###

def _sqlite_sign(x: Optional[float]) -> Optional[int]:
    if x is None:
        return None
    return (x > 0) - (x < 0)

### SECTION SEPARATOR ###

def _sqlite_sin(x: Optional[float]) -> Optional[float]:
    if x is None:
        return None
    return sin(x)

### SECTION SEPARATOR ###

def _sqlite_sqrt(x: Optional[float]) -> Optional[float]:
    if x is None:
        return None
    return sqrt(x)

### SECTION SEPARATOR ###

def _sqlite_tan(x: Optional[float]) -> Optional[float]:
    if x is None:
        return None
    return tan(x)

### SECTION SEPARATOR ###

class ListAggregate(list):
    step: Callable[[list, float], None] = list.append

### SECTION SEPARATOR ###

class StdDevPop(ListAggregate):
    finalize: Callable[[list], float] = statistics.pstdev

### SECTION SEPARATOR ###

class StdDevSamp(ListAggregate):
    finalize: Callable[[list], float] = statistics.stdev

### SECTION SEPARATOR ###

class VarPop(ListAggregate):
    finalize: Callable[[list], float] = statistics.pvariance

### SECTION SEPARATOR ###

class VarSamp(ListAggregate):
    finalize: Callable[[list], float] = statistics.variance
