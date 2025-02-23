"""
Functions and routines associated with Enasis Network Common Library.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from time import sleep

from pytest import fixture

from ..time import Time
from ..timer import Timer
from ...types import inrepr
from ...types import instr
from ...types import lattrs



@fixture
def timer() -> Timer:
    """
    Construct the instance for use in the downstream tests.

    :returns: Newly constructed instance of related class.
    """

    return Timer(1)



def test_Timer(
    timer: Timer,
) -> None:
    """
    Perform various tests associated with relevant routines.

    :param timer: Primary class instance for timer object.
    """


    attrs = lattrs(timer)

    assert attrs == [
        '_Timer__timer',
        '_Timer__time']


    assert inrepr(
        'timer.Timer object',
        timer)

    assert isinstance(
        hash(timer), int)

    assert instr(
        'timer.Timer object',
        timer)


    assert timer.timer == 1

    assert timer.time >= Time('-1s')

    assert timer.since <= 1

    assert timer.remains <= 1

    assert not timer.ready()
    assert timer.pause()


    sleep(1)

    assert timer.since > 1

    assert timer.remains == 0

    assert timer.ready()
    assert timer.pause()

    assert not timer.ready()
    assert timer.pause()

    timer.update('1980-01-01')

    assert timer.ready()
    assert timer.pause()

    assert not timer.ready()
    assert timer.pause()
