"""
Functions and routines associated with Enasis Network Common Library.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from copy import copy
from datetime import datetime
from datetime import timedelta
from typing import Optional

from croniter import croniter

from .common import PARSABLE
from .common import SCHEDULE
from .parse import parse_time
from .time import Time



class Window:
    """
    Process and operate crontab or interval based schedule.

    .. testsetup::
       >>> from time import sleep

    Example
    -------
    >>> window = Window('* * * * *', '-4m@m')
    >>> [window.ready() for _ in range(5)]
    [True, True, True, True, False]

    :param window: Parameters for defining scheduled time.
    :param start: Determine the start for scheduling window.
    :param stop: Determine the ending for scheduling window.
    :param anchor: Optionally define time anchor for window.
    :param delay: Period of time schedulng will be delayed.
    """

    __window: SCHEDULE
    __start: Time
    __stop: Time
    __anchor: Time
    __delay: float

    __wlast: Time
    __wnext: Time


    def __init__(
        self,
        window: SCHEDULE,
        start: Optional[PARSABLE] = None,
        stop: Optional[PARSABLE] = None,
        *,
        anchor: Optional[PARSABLE] = None,
        delay: float = 0,
    ) -> None:
        """
        Initialize instance for class using provided parameters.
        """

        anchor = anchor or start

        window = copy(window)
        start = Time(start)
        stop = Time(stop)
        anchor = Time(anchor)
        delay = float(delay)

        assert stop > start


        self.__window = window
        self.__start = start
        self.__stop = stop
        self.__anchor = anchor
        self.__delay = delay


        wlast, wnext = (
            self.__helper(anchor))

        while wnext > start:
            wlast, wnext = (
                self.__helper(wlast, True))

        while wnext < start:
            wlast, wnext = (
                self.__helper(wnext, False))

        self.__wlast = wlast
        self.__wnext = wnext



    @property
    def window(
        self,
    ) -> SCHEDULE:
        """
        Return the value for the attribute from class instance.

        :returns: Value for the attribute from class instance.
        """

        return copy(self.__window)


    @property
    def start(
        self,
    ) -> Time:
        """
        Return the value for the attribute from class instance.

        :returns: Value for the attribute from class instance.
        """

        return Time(self.__start)


    @property
    def stop(
        self,
    ) -> Time:
        """
        Return the value for the attribute from class instance.

        :returns: Value for the attribute from class instance.
        """

        return Time(self.__stop)


    @property
    def anchor(
        self,
    ) -> Time:
        """
        Return the value for the attribute from class instance.

        :returns: Value for the attribute from class instance.
        """

        return Time(self.__anchor)


    @property
    def delay(
        self,
    ) -> float:
        """
        Return the value for the attribute from class instance.

        :returns: Value for the attribute from class instance.
        """

        return float(self.__delay)


    @property
    def last(
        self,
    ) -> Time:
        """
        Return the value for the attribute from class instance.

        :returns: Value for the attribute from class instance.
        """

        return Time(self.__wlast)


    @property
    def next(
        self,
    ) -> Time:
        """
        Return the value for the attribute from class instance.

        :returns: Value for the attribute from class instance.
        """

        return Time(self.__wnext)


    @property
    def soonest(
        self,
    ) -> Time:
        """
        Return the value for the attribute from class instance.

        :returns: Value for the attribute from class instance.
        """
        return Time(Time() - self.delay)


    @property
    def latest(
        self,
    ) -> Time:
        """
        Return the value for the attribute from class instance.

        :returns: Value for the attribute from class instance.
        """
        return Time(self.stop - self.delay)


    @property
    def walked(
        self,
    ) -> bool:
        """
        Return the value for the attribute from class instance.

        :returns: Value for the attribute from class instance.
        """

        return self.next >= self.latest


    def __helper(
        self,
        anchor: PARSABLE,
        backward: bool = False,
    ) -> tuple[Time, Time]:
        """
        Determine next and last windows for window using anchor.

        :param anchor: Optionally define time anchor for window.
        :param backward: Optionally operate the window backward.
        :returns: Next and previous windows for schedule window.
        """

        window = self.__window

        if isinstance(window, str):
            return window_croniter(
                window, anchor, backward)

        if isinstance(window, dict):
            return window_interval(
                window, anchor, backward)

        raise NotImplementedError


    def ready(  # noqa: CFQ004
        self,
        update: bool = True,
    ) -> bool:
        """
        Walk the internal time using current position in schedule.

        :param update: Determines whether or not time is updated.
        :returns: Boolean indicating outcome from the operation.
        """

        wnext = self.__wnext

        walked = self.walked
        soonest = self.soonest


        if walked is True:
            return False

        if wnext > soonest:
            return False


        wlast, wnext = (
            self.__helper(wnext))

        if update is True:
            self.__wlast = wlast
            self.__wnext = wnext

        if wnext > soonest:
            return False

        return True


    def update(
        self,
        value: Optional[PARSABLE] = None,
    ) -> None:
        """
        Update the window from the provided parasable time value.

        :param value: Override the time updated for window value.
        """

        value = Time(
            value or 'now')

        wlast, wnext = (
            self.__helper(value))

        self.__wlast = wlast
        self.__wnext = wnext



def window_croniter(  # noqa: CFQ004
    schedule: str,
    anchor: PARSABLE,
    backward: bool = False,
) -> tuple[Time, Time]:
    """
    Determine next and previous times for cronjob schedule.

    :param window: Parameters for defining scheduled time.
    :param anchor: Optionally define time anchor for window.
    :param backward: Optionally operate the window backward.
    :returns: Next and previous windows for schedule window.
    """

    anchor = parse_time(anchor)


    def _wnext(
        source: datetime,
    ) -> datetime:

        source = (
            _operator(source)
            .get_next())

        return parse_time(source)


    def _wlast(
        source: datetime,
    ) -> datetime:

        source = (
            _operator(source)
            .get_prev())

        return parse_time(source)


    def _operator(
        source: datetime,
    ) -> croniter:
        return croniter(
            schedule, source)


    wnext = _wnext(anchor)

    if backward is True:
        wnext = _wlast(wnext)

    wlast = _wlast(wnext)


    return (
        Time(wlast),
        Time(wnext))



def window_interval(
    schedule: dict[str, int],
    anchor: PARSABLE,
    backward: bool = False,
) -> tuple[Time, Time]:
    """
    Determine next and previous times for interval schedule.

    :param window: Parameters for defining scheduled time.
    :param anchor: Optionally define time anchor for window.
    :param backward: Optionally operate the window backward.
    :returns: Next and previous windows for schedule window.
    """

    anpoch = (
        parse_time(anchor)
        .timestamp())

    seconds = (
        timedelta(**schedule)
        .seconds)


    if backward is True:
        wnext = anpoch
        wlast = anpoch - seconds

    else:
        wnext = anpoch + seconds
        wlast = anpoch


    return (
        Time(wlast),
        Time(wnext))
