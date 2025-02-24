"""
Functions and routines associated with Enasis Network Common Library.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from typing import Optional

from .common import NUMERIC
from .common import PARSABLE
from .time import Time



class Timer:
    """
    Process and operate the timer using provided interval.

    .. testsetup::
       >>> from time import sleep

    Example
    -------
    >>> timer = Timer(1)
    >>> timer.ready()
    False
    >>> sleep(1)
    >>> timer.ready()
    True

    :param seconds: Period of time which must pass in timer.
    :param started: Override default of using current time.
    """

    __timer: float
    __time: Time


    def __init__(
        self,
        timer: NUMERIC,
        *,
        start: Optional[PARSABLE] = None,
    ) -> None:
        """
        Initialize instance for class using provided parameters.
        """

        timer = float(timer)
        start = Time(start)

        self.__timer = timer
        self.__time = start


    @property
    def timer(
        self,
    ) -> float:
        """
        Return the value for the attribute from class instance.

        :returns: Value for the attribute from class instance.
        """

        return self.__timer


    @property
    def time(
        self,
    ) -> Time:
        """
        Return the value for the attribute from class instance.

        :returns: Value for the attribute from class instance.
        """

        return self.__time


    @property
    def since(
        self,
    ) -> float:
        """
        Return the seconds that have elapsed since the interval.

        :returns: Seconds that have elapsed since the interval.
        """

        return self.time.since


    @property
    def remains(
        self,
    ) -> float:
        """
        Return the value for the attribute from class instance.

        :returns: Value for the attribute from class instance.
        """

        timer = self.timer
        since = self.since

        return max(0.0, timer - since)


    def ready(
        self,
        update: bool = True,
    ) -> bool:
        """
        Determine whether or not the appropriate time has passed.

        :param update: Determines whether or not time is updated.
        :returns: Boolean indicating whether enough time passed.
        """

        if self.remains > 0:
            return False

        if update is True:
            self.update('now')

        return True


    def pause(
        self,
        update: bool = True,
    ) -> bool:
        """
        Determine whether or not the appropriate time has passed.

        :param update: Determines whether or not time is updated.
        :returns: Boolean indicating whether enough time passed.
        """

        return not self.ready(update)


    def update(
        self,
        value: Optional[PARSABLE] = None,
    ) -> None:
        """
        Update the timer from the provided parasable time value.

        :param value: Override the time updated for timer value.
        """

        value = Time(
            value or 'now')

        self.__time = value
