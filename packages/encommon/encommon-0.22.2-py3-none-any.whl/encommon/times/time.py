"""
Functions and routines associated with Enasis Network Common Library.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from contextlib import suppress
from datetime import datetime
from datetime import time as dtime
from datetime import timedelta
from typing import Optional

from .common import PARSABLE
from .common import STAMP_HUMAN
from .common import STAMP_SIMPLE
from .common import STAMP_SUBSEC
from .parse import parse_time
from .parse import since_time
from .utils import findtz
from .utils import strftime



class Time:
    """
    Interact with various time functions through one wrapper.

    .. testsetup::
       >>> time = Time('1/1/2000 12:00am')

    Example
    -------
    >>> time = Time('1/1/2000 12:00am')
    >>> time.stamp()
    '2000-01-01T00:00:00.000000+0000'
    >>> time.stamp('%m/%d/%Y')
    '01/01/2000'

    Example
    -------
    >>> time.epoch
    946684800.0
    >>> time.time
    datetime.time(0, 0)
    >>> time.simple
    '2000-01-01T00:00:00+0000'
    >>> time.human
    '01/01/2000 12:00AM UTC'

    Example
    -------
    >>> time.before
    Time('1999-12-31T23:59:59.999999+0000')
    >>> time.after
    Time('2000-01-01T00:00:00.000001+0000')

    Example
    -------
    >>> time.shift('-1d')
    Time('1999-12-31T00:00:00.000000+0000')

    Example
    -------
    >>> time.shifz('US/Central')
    Time('1999-12-31T18:00:00.000000-0600')

    Example
    -------
    >>> time = Time('-1s')
    >>> int(time.since)
    1

    Example
    -------
    >>> time1 = Time('1/1/2000 12:00am')
    >>> time2 = Time('1/1/2000 12:00am')
    >>> time1 - time2
    0.0
    >>> time1 + time2
    1893369600.0

    :param source: Time in various forms that will be parsed.
    :param anchor: Optional relative time; for snap notation.
    :param format: Optional format when source is timestamp.
    :param tzname: Name of the timezone associated to source.
        This is not relevant in timezone included in source.
    """

    __source: datetime


    def __init__(
        self,
        source: Optional[PARSABLE] = None,
        *,
        anchor: Optional[PARSABLE] = None,
        format: str = STAMP_SUBSEC,
        tzname: Optional[str] = None,
    ) -> None:
        """
        Initialize instance for class using provided parameters.
        """

        parsed = parse_time(
            source=source,
            anchor=anchor,
            format=format,
            tzname=tzname)

        self.__source = parsed


    def __repr__(
        self,
    ) -> str:
        """
        Built-in method for representing the values for instance.

        :returns: String representation for values from instance.
        """

        return f"Time('{self.subsec}')"


    def __hash__(
        self,
    ) -> int:
        """
        Built-in method called when performing hashing operation.

        :returns: Boolean indicating outcome from the operation.
        """

        return hash(self.__source)


    def __str__(
        self,
    ) -> str:
        """
        Built-in method for representing the values for instance.

        :returns: String representation for values from instance.
        """

        return self.stamp()


    def __int__(
        self,
    ) -> int:
        """
        Built-in method representing numeric value for instance.

        :returns: Numeric representation for value in instance.
        """

        return int(self.epoch)


    def __float__(
        self,
    ) -> float:
        """
        Built-in method representing numeric value for instance.

        :returns: Numeric representation for value in instance.
        """

        return float(self.epoch)


    def __add__(
        self,
        other: PARSABLE,
    ) -> float:
        """
        Built-in method for mathematically processing the value.

        :param other: Other value being compared with instance.
        :returns: Python timedelta object containing the answer.
        """

        parsed = (
            parse_time(other)
            .timestamp())

        return self.epoch + parsed


    def __sub__(
        self,
        other: PARSABLE,
    ) -> float:
        """
        Built-in method for mathematically processing the value.

        :param other: Other value being compared with instance.
        :returns: Python timedelta object containing the answer.
        """

        parsed = (
            parse_time(other)
            .timestamp())

        return self.epoch - parsed


    def __eq__(
        self,
        other: object,
    ) -> bool:
        """
        Built-in method for comparing this instance with another.

        :param other: Other value being compared with instance.
        :returns: Boolean indicating outcome from the operation.
        """

        source = self.__source

        with suppress(Exception):

            parsed = parse_time(
                other)  # type: ignore

            return source == parsed

        return False


    def __ne__(
        self,
        other: object,
    ) -> bool:
        """
        Built-in method for comparing this instance with another.

        :param other: Other value being compared with instance.
        :returns: Boolean indicating outcome from the operation.
        """

        return not self.__eq__(other)


    def __gt__(
        self,
        other: PARSABLE,
    ) -> bool:
        """
        Built-in method for comparing this instance with another.

        :param other: Other value being compared with instance.
        :returns: Boolean indicating outcome from the operation.
        """

        parsed = parse_time(other)

        return self.__source > parsed


    def __ge__(
        self,
        other: PARSABLE,
    ) -> bool:
        """
        Built-in method for comparing this instance with another.

        :param other: Other value being compared with instance.
        :returns: Boolean indicating outcome from the operation.
        """

        parsed = parse_time(other)

        return self.__source >= parsed


    def __lt__(
        self,
        other: PARSABLE,
    ) -> bool:
        """
        Built-in method for comparing this instance with another.

        :param other: Other value being compared with instance.
        :returns: Boolean indicating outcome from the operation.
        """

        parsed = parse_time(other)

        return self.__source < parsed


    def __le__(
        self,
        other: PARSABLE,
    ) -> bool:
        """
        Built-in method for comparing this instance with another.

        :param other: Other value being compared with instance.
        :returns: Boolean indicating outcome from the operation.
        """

        parsed = parse_time(other)

        return self.__source <= parsed


    @property
    def source(
        self,
    ) -> datetime:
        """
        Return the value for the attribute from class instance.

        :returns: Value for the attribute from class instance.
        """

        return self.__source


    @property
    def epoch(
        self,
    ) -> float:
        """
        Return the seconds since the Unix epoch for the instance.

        :returns: Seconds since the Unix epoch for the instance.
        """

        source = self.__source

        return source.timestamp()


    @property
    def spoch(
        self,
    ) -> int:
        """
        Return the seconds since the Unix epoch for the instance.

        :returns: Seconds since the Unix epoch for the instance.
        """

        return int(self.epoch)


    @property
    def mpoch(
        self,
    ) -> float:
        """
        Return milliseconds since the Unix epoch for the instance.

        :returns: Seconds since the Unix epoch for the instance.
        """

        return self.epoch * 1000


    @property
    def time(
        self,
    ) -> dtime:
        """
        Return the value for the attribute from class instance.

        :returns: Value for the attribute from class instance.
        """

        return self.__source.time()


    @property
    def simple(
        self,
    ) -> str:
        """
        Return the value for the attribute from class instance.

        :returns: Value for the attribute from class instance.
        """

        return self.stamp(STAMP_SIMPLE)


    @property
    def subsec(
        self,
    ) -> str:
        """
        Return the value for the attribute from class instance.

        :returns: Value for the attribute from class instance.
        """

        return self.stamp(STAMP_SUBSEC)


    @property
    def human(
        self,
    ) -> str:
        """
        Return the value for the attribute from class instance.

        :returns: Value for the attribute from class instance.
        """

        return self.stamp(STAMP_HUMAN)


    @property
    def elapsed(
        self,
    ) -> float:
        """
        Determine the time in seconds occurring since instance.

        :returns: Time in seconds occurring since the instance.
        """

        return since_time(self.__source)


    @property
    def since(
        self,
    ) -> float:
        """
        Determine the time in seconds occurring since instance.

        :returns: Time in seconds occurring since the instance.
        """

        return since_time(self.__source)


    @property
    def before(
        self,
    ) -> 'Time':
        """
        Return new object containing time just before the time.

        :returns: Object containing time just before the time.
        """

        source = self.__source

        source -= timedelta(
            microseconds=1)

        return Time(source)


    @property
    def after(
        self,
    ) -> 'Time':
        """
        Return new object containing time just after the time.

        :returns: Object containing time just after the time.
        """

        source = self.__source

        source += timedelta(
            microseconds=1)

        return Time(source)


    def stamp(
        self,
        format: str = STAMP_SUBSEC,
        tzname: Optional[str] = None,
    ) -> str:
        """
        Return the timestamp using provided format for instance.

        :param format: Optional format when source is timestamp.
        :param tzname: Name of the timezone associated to source.
            This is not relevant in timezone included in source.
        :returns: Timestamp using provided format for instance.
        """

        source = self.__source

        tzinfo = findtz(tzname)

        if tzname is not None:

            source = (
                source
                .astimezone(tzinfo))

        return strftime(
            source, format)


    def shift(
        self,
        notate: str,
    ) -> 'Time':
        """
        Return the new instance of object shifted using snaptime.

        :param notate: Syntax compatable using snaptime library.
        :returns: New instance of the class using shifted time.
        """

        source = self.__source

        return Time(
            notate, anchor=source)


    def shifz(
        self,
        tzname: str,
    ) -> 'Time':
        """
        Return the new instance of object shifted using datetime.

        :param tzname: Name of the timezone associated to source.
            This is not relevant in timezone included in source.
        :returns: New instance of the class using shifted time.
        """

        source = self.__source

        tzinfo = findtz(tzname)

        if tzname is not None:

            source = (
                source
                .astimezone(tzinfo))

        return Time(
            source, tzname=tzname)
