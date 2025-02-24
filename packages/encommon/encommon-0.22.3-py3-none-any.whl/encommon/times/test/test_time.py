"""
Functions and routines associated with Enasis Network Common Library.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from ..common import STAMP_SIMPLE
from ..common import UNIXEPOCH
from ..common import UNIXHPOCH
from ..common import UNIXMPOCH
from ..time import Time
from ...types import inrepr
from ...types import instr
from ...types import lattrs



def test_Time() -> None:
    """
    Perform various tests associated with relevant routines.
    """

    time = Time(
        UNIXEPOCH,
        format=STAMP_SIMPLE)


    attrs = lattrs(time)

    assert attrs == [
        '_Time__source']


    assert inrepr(
        "Time('1970-01-01T00:00",
        time)

    assert isinstance(
        hash(time), int)

    assert instr(
        '1970-01-01T00:00:00.000',
        time)


    assert int(time) == 0
    assert float(time) == 0.0

    assert time + 1 == Time(1)
    assert time - 1 == Time(-1)

    assert time == Time(0)
    assert time != Time(-1)
    assert time != 'invalid'

    assert time > Time(-1)
    assert time >= Time(0)
    assert time < Time(1)
    assert time <= Time(0)


    assert time.source.year == 1970

    assert time.epoch == 0.0

    assert time.spoch == 0

    assert time.mpoch == 0.0

    assert str(time.time) == '00:00:00'

    assert time.simple == UNIXEPOCH

    assert time.subsec == UNIXMPOCH

    assert time.human == UNIXHPOCH

    assert time.elapsed >= 1672531200

    assert time.since >= 1672531200

    assert time.before == (
        '1969-12-31T23:59:59.999999Z')

    assert time.after == (
        '1970-01-01T00:00:00.000001Z')

    assert time.stamp() == UNIXMPOCH

    time = time.shift('+1y')
    assert time == '1971-01-01'

    time = time.shifz('UTC-1')
    assert time == (
        '12/31/1970 23:00 -0100')



def test_Time_tzname() -> None:
    """
    Perform various tests associated with relevant routines.
    """

    time1 = Time(
        '1970-01-01T00:00:00Z')

    time2 = time1.shifz(
        'US/Central')


    delta = time1 - time2

    assert -1 < delta < 1


    stamp1 = time1.stamp(
        tzname='US/Central')

    stamp2 = time2.stamp()

    assert stamp1 == stamp2
