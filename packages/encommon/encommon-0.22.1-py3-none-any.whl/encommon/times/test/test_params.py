"""
Functions and routines associated with Enasis Network Common Library.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from ..params import TimerParams
from ..params import WindowParams



def test_TimerParams() -> None:
    """
    Perform various tests associated with relevant routines.
    """

    params = TimerParams(
        timer=1,
        start='1980-01-01T00:00:00Z')

    assert params.start == (
        '1980-01-01T00:00:00.000000+0000')



def test_WindowParams() -> None:
    """
    Perform various tests associated with relevant routines.
    """


    params = WindowParams(
        window='* * * * *',
        start='1980-01-01T00:00:00Z',
        stop='1980-01-02T00:00:00Z',
        anchor='1980-01-01T00:00:00Z',
        delay=10)

    assert params.start == (
        '1980-01-01T00:00:00.000000+0000')

    assert params.stop == (
        '1980-01-02T00:00:00.000000+0000')

    assert str(params.delay) == '10.0'


    params = WindowParams(
        window=60,
        start='1980-01-01T00:00:00Z',
        stop='1980-01-02T00:00:00Z',
        anchor='1980-01-01T00:00:00Z',
        delay=10)

    assert params.start == (
        '1980-01-01T00:00:00.000000+0000')

    assert params.stop == (
        '1980-01-02T00:00:00.000000+0000')

    assert str(params.delay) == '10.0'
