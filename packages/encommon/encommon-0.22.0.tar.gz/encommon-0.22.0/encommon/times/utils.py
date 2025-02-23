"""
Functions and routines associated with Enasis Network Common Library.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from contextlib import suppress
from datetime import datetime
from datetime import timezone
from datetime import tzinfo
from typing import Any
from typing import Optional

from dateutil.tz import gettz



def findtz(
    tzname: Optional[str] = None,
) -> tzinfo:
    """
    Return the located timezone object for the provided name.

    Example
    -------
    >>> findtz('US/Central')
    tzfile('/usr/share/zoneinfo/US/Central')

    :param tzname: Name of the timezone associated to source.
    :returns: Located timezone object for the provided name.
    """

    if tzname is None:
        return timezone.utc

    tzinfo = gettz(tzname)

    if tzinfo is None:
        raise ValueError('tzname')

    return tzinfo



def utcdatetime(
    *args: Any,
    **kwargs: Any,
) -> datetime:
    """
    Return the instance of datetime within the UTC timezone.

    .. warning::
       If no arguments are provided, returns current time.

    Example
    -------
    >>> utcdatetime(1970, 1, 1)
    datetime.datetime(1970, 1, 1, 0...

    :param args: Positional arguments passed for downstream.
    :param kwargs: Keyword arguments passed for downstream.
    :returns: Instance of datetime within the UTC timezone.
    """

    tzinfo = timezone.utc

    if not args and not kwargs:
        return datetime.now(tz=tzinfo)

    if 'tzinfo' not in kwargs:
        kwargs['tzinfo'] = tzinfo

    return (
        datetime(*args, **kwargs)
        .astimezone(timezone.utc))



def strptime(
    source: str,
    formats: str | list[str],
) -> datetime:
    """
    Parse provided time value with various supported formats.

    Example
    -------
    >>> strptime('2023', '%Y')
    datetime.datetime(2023, 1, 1, 0...

    :param source: Time in various forms that will be parsed.
    :param formats: Various formats compatable with strptime.
    :returns: Python datetime object containing related time.
    """

    tzinfo = timezone.utc

    if isinstance(formats, str):
        formats = [formats]


    def _strptime(
        format: str,
    ) -> datetime:

        return (
            datetime
            .strptime(source, format)
            .astimezone(tzinfo))


    for format in formats:

        with suppress(ValueError):
            return _strptime(format)


    raise ValueError('invalid')



def strftime(
    source: datetime,
    format: str,
) -> str:
    """
    Return the timestamp string for datetime object provided.

    .. note::
       This function is extremely pedantic and cosmetic.

    Example
    -------
    >>> dtime = datetime(2023, 1, 1)
    >>> strftime(dtime, '%Y')
    '2023'

    :param source: Python datetime instance containing source.
    :param format: Format for the timestamp string returned.
    :returns: Timestamp string for datetime object provided.
    """

    return (
        datetime
        .strftime(source, format))
