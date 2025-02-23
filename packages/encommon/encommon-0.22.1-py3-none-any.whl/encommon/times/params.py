"""
Functions and routines associated with Enasis Network Common Library.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from typing import Annotated
from typing import Optional

from pydantic import Field

from .common import PARSABLE
from .common import SCHEDULE
from .time import Time
from ..types import BaseModel
from ..types import DictStrAny



_TIMERS = dict[str, 'TimerParams']
_WINDOWS = dict[str, 'WindowParams']



class TimerParams(BaseModel, extra='forbid'):
    """
    Process and validate the core configuration parameters.
    """

    timer: Annotated[
        float,
        Field(...,
              description='Seconds used for the interval')]

    start: Annotated[
        str,
        Field(...,
              description='Optional value of timer start',
              min_length=1)]


    def __init__(
        self,
        timer: int | float,
        start: PARSABLE = 'now',
    ) -> None:
        """
        Initialize instance for class using provided parameters.
        """

        data: DictStrAny = {}


        if timer is not None:
            timer = float(timer)

        if start is not None:
            start = Time(start)


        data['timer'] = timer

        if start is not None:
            data['start'] = start.subsec


        super().__init__(**data)



class TimersParams(BaseModel, extra='forbid'):
    """
    Process and validate the core configuration parameters.
    """

    timers: Annotated[
        _TIMERS,
        Field(...,
              description='Seconds used for the interval',
              min_length=0)]


    def __init__(
        self,
        timers: Optional[_TIMERS] = None,
    ) -> None:
        """
        Initialize instance for class using provided parameters.
        """

        timers = timers or {}

        super().__init__(**{
            'timers': timers})



class WindowParams(BaseModel, extra='forbid'):
    """
    Process and validate the core configuration parameters.
    """

    window: Annotated[
        SCHEDULE,
        Field(...,
              description='Period for scheduling window',
              min_length=1)]

    start: Annotated[
        Optional[str],
        Field(None,
              description='Determine when scope begins',
              min_length=1)]

    stop: Annotated[
        Optional[str],
        Field(None,
              description='Determine when scope ends',
              min_length=1)]

    anchor: Annotated[
        Optional[str],
        Field(None,
              description='Optional anchor of the window',
              min_length=1)]

    delay: Annotated[
        float,
        Field(...,
              description='Time period of schedule delay',
              ge=0)]


    def __init__(
        self,
        window: SCHEDULE | int,
        *,
        start: Optional[PARSABLE] = None,
        stop: Optional[PARSABLE] = None,
        anchor: Optional[PARSABLE] = None,
        delay: int | float = 0.0,
    ) -> None:
        """
        Initialize instance for class using provided parameters.
        """

        data: DictStrAny = {}


        if isinstance(window, int):
            window = {'seconds': window}

        if start is not None:
            start = Time(start)

        if stop is not None:
            stop = Time(stop)

        if anchor is not None:
            anchor = Time(anchor)

        delay = float(delay)


        data['window'] = window

        if start is not None:
            data['start'] = start.subsec

        if stop is not None:
            data['stop'] = stop.subsec

        if anchor is not None:
            data['anchor'] = anchor.subsec

        data['delay'] = delay


        super().__init__(**data)



class WindowsParams(BaseModel, extra='forbid'):
    """
    Process and validate the core configuration parameters.
    """

    windows: Annotated[
        _WINDOWS,
        Field(...,
              description='Period for scheduling windows',
              min_length=0)]


    def __init__(
        self,
        windows: Optional[_WINDOWS] = None,
    ) -> None:
        """
        Initialize instance for class using provided parameters.
        """

        windows = windows or {}

        super().__init__(**{
            'windows': windows})
