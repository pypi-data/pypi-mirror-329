"""
Functions and routines associated with Enasis Network Common Library.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from time import sleep
from typing import TYPE_CHECKING

from pytest import fixture
from pytest import mark

from ..time import Time
from ..window import Window
from ..window import window_croniter
from ..window import window_interval
from ...types import inrepr
from ...types import instr
from ...types import lattrs

if TYPE_CHECKING:
    from ..common import PARSABLE



@fixture
def window() -> Window:
    """
    Construct the instance for use in the downstream tests.

    :returns: Newly constructed instance of related class.
    """

    return Window(
        window='* * * * *',
        start=300,
        stop=600,
        delay=10)



def test_Window(
    window: Window,
) -> None:
    """
    Perform various tests associated with relevant routines.

    :param window: Primary class instance for window object.
    """


    attrs = lattrs(window)

    assert attrs == [
        '_Window__window',
        '_Window__start',
        '_Window__stop',
        '_Window__anchor',
        '_Window__delay',
        '_Window__wlast',
        '_Window__wnext']


    assert inrepr(
        'window.Window object',
        window)

    assert isinstance(
        hash(window), int)

    assert instr(
        'window.Window object',
        window)


    assert window.window == '* * * * *'

    assert window.start == (
        '1970-01-01T00:05:00Z')

    assert window.stop == (
        '1970-01-01T00:10:00Z')

    assert window.anchor == window.start

    assert str(window.delay) == '10.0'

    assert window.last == (
        '1970-01-01T00:04:00Z')

    assert window.next == (
        '1970-01-01T00:05:00Z')

    assert window.latest == (
        '1970-01-01T00:09:50Z')

    assert not window.walked



def test_Window_cover(
    window: Window,
) -> None:
    """
    Perform various tests associated with relevant routines.

    :param window: Primary class instance for window object.
    """


    window = Window(
        window={'minutes': 1},
        start=window.start,
        stop=window.stop)

    assert window.last == (
        '1970-01-01T00:04:00Z')

    assert window.next == (
        '1970-01-01T00:05:00Z')

    assert not window.walked

    for count in range(100):
        if window.walked:
            break
        assert window.ready()

    assert count == 5
    assert not window.ready()

    assert window.last == (
        '1970-01-01T00:09:00Z')

    assert window.next == (
        '1970-01-01T00:10:00Z')

    assert window.walked


    window = Window(
        window='* * * * *',
        start=window.start,
        stop=window.stop)

    assert window.last == (
        '1970-01-01T00:04:00Z')

    assert window.next == (
        '1970-01-01T00:05:00Z')

    assert not window.walked

    for count in range(100):
        if window.walked:
            break
        assert window.ready()

    assert count == 5
    assert not window.ready()

    assert window.last == (
        '1970-01-01T00:09:00Z')

    assert window.next == (
        '1970-01-01T00:10:00Z')

    assert window.walked


    anchor = Time('-0s@s')


    window = Window(
        window='* * * * *',
        start=anchor.shift('+5m'),
        stop=anchor.shift('+10m'))

    assert not window.ready(False)


    window = Window(
        window={'seconds': 1},
        start=anchor.shift('-5s'),
        stop=anchor.shift('+5s'))

    assert not window.walked

    for count in range(100):
        if window.walked:
            break
        if window.ready():
            continue
        sleep(0.25)

    assert 16 <= count <= 32
    assert not window.ready()

    assert window.walked



@mark.parametrize(
    'window,anchor,backward,expect',
    [('* * * * *', 0, False, (0, 60)),
     ('* * * * *', 1, False, (0, 60)),
     ('* * * * *', 0, True, (-60, 0)),
     ('* * * * *', 1, True, (-60, 0)),
     ('* * * * *', 3559, False, (3540, 3600)),
     ('* * * * *', 3659, False, (3600, 3660)),
     ('* * * * *', 3660, False, (3660, 3720)),
     ('* * * * *', 3661, False, (3660, 3720)),
     ('0 * * * *', 3559, False, (0, 3600)),
     ('0 * * * *', 3660, False, (3600, 7200)),
     ('0 * * * *', 3661, False, (3600, 7200))])
def test_window_croniter(
    window: str,
    anchor: 'PARSABLE',
    backward: bool,
    expect: tuple[int, int],
) -> None:
    """
    Perform various tests associated with relevant routines.

    :param window: Parameters for defining scheduled time.
    :param anchor: Optionally define time anchor for window.
    :param backward: Optionally operate the window backward.
    :param expect: Expected output from the testing routine.
    """

    croniter = window_croniter(
        window, anchor, backward)

    assert croniter[0] == expect[0]
    assert croniter[1] == expect[1]



@mark.parametrize(
    'window,anchor,backward,expect',
    [({'seconds': 60}, 0, False, (0, 60)),
     ({'seconds': 60}, 1, False, (1, 61)),
     ({'seconds': 60}, 0, True, (-60, 0)),
     ({'seconds': 60}, 1, True, (-59, 1)),
     ({'seconds': 60}, 3559, False, (3559, 3619)),
     ({'seconds': 60}, 3659, False, (3659, 3719)),
     ({'seconds': 60}, 3660, False, (3660, 3720)),
     ({'seconds': 60}, 3661, False, (3661, 3721)),
     ({'hours': 1}, 3559, False, (3559, 7159)),
     ({'hours': 1}, 3660, False, (3660, 7260)),
     ({'hours': 1}, 3661, False, (3661, 7261))])
def test_window_interval(
    window: dict[str, int],
    anchor: 'PARSABLE',
    backward: bool,
    expect: tuple[int, int],
) -> None:
    """
    Perform various tests associated with relevant routines.

    :param window: Parameters for defining scheduled time.
    :param anchor: Optionally define time anchor for window.
    :param backward: Optionally operate the window backward.
    :param expect: Expected output from the testing routine.
    """

    interval = window_interval(
        window, anchor, backward)

    assert interval[0] == expect[0]
    assert interval[1] == expect[1]
