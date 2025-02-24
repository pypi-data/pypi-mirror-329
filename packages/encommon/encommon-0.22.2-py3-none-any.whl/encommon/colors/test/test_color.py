"""
Functions and routines associated with Enasis Network Common Library.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from pytest import mark

from ..color import Color
from ...types import lattrs



def test_Color() -> None:
    """
    Perform various tests associated with relevant routines.
    """

    color = Color('000001')


    attrs = lattrs(color)

    assert attrs == [
        '_Color__source']


    assert repr(color) == (
        "Color('#000001')")

    assert isinstance(
        hash(color), int)

    assert str(color) == '#000001'


    assert int(color) == 1
    assert float(color) == 1.0

    assert color + 1 == '000002'
    assert color - 1 == '000000'

    assert color == '000001'
    assert color != '000000'
    assert color != int  # noqa

    assert color > 0
    assert color >= 1
    assert color <= 1
    assert color < 2

    assert color > '000000'
    assert color >= '000001'
    assert color <= '000001'
    assert color < '000002'



@mark.parametrize(
    'source,expect',
    [('ff00cc', (255, 0, 204)),
     ('ffffff', (255, 255, 255)),
     ('000000', (0, 0, 0)),
     ('ff0000', (255, 0, 0)),
     ('00ff00', (0, 255, 0)),
     ('0000ff', (0, 0, 255)),
     ('808080', (128, 128, 128)),
     ('ffff00', (255, 255, 0)),
     ('00ffff', (0, 255, 255)),
     ('ff00ff', (255, 0, 255)),
     ('800080', (128, 0, 128))])
def test_Color_rgb(
    source: str,
    expect: tuple[int, ...],
) -> None:
    """
    Perform various tests associated with relevant routines.

    :param source: Source color used when converting values.
    :param expect: Expected output from the testing routine.
    """

    assert Color(source).rgb == expect



@mark.parametrize(
    'source,expect',
    [('ff00cc', (52.1391, 25.6196, 59.3238)),
     ('ffffff', (95.0500, 100.0000, 108.9000)),
     ('000000', (0.0000, 0.0000, 0.0000)),
     ('ff0000', (41.2400, 21.2600, 1.9300)),
     ('00ff00', (35.7600, 71.5200, 11.9200)),
     ('0000ff', (18.0500, 7.2200, 95.0500)),
     ('808080', (20.5175, 21.5861, 23.5072)),
     ('ffff00', (77.0000, 92.7800, 13.8500)),
     ('00ffff', (53.8100, 78.7400, 106.9700)),
     ('ff00ff', (59.2900, 28.4800, 96.9800)),
     ('800080', (12.7984, 6.1477, 20.9342))])
def test_Color_xyz(
    source: str,
    expect: tuple[int, ...],
) -> None:
    """
    Perform various tests associated with relevant routines.

    :param source: Source color used when converting values.
    :param expect: Expected output from the testing routine.
    """

    assert Color(source).xyz == expect



@mark.parametrize(
    'source,expect',
    [('ff00cc', (0.3803, 0.1869)),
     ('ffffff', (0.3127, 0.3290)),
     ('000000', (0.0000, 0.0000)),
     ('ff0000', (0.6401, 0.3300)),
     ('00ff00', (0.3000, 0.6000)),
     ('0000ff', (0.1500, 0.0600)),
     ('808080', (0.3127, 0.3290)),
     ('ffff00', (0.4193, 0.5053)),
     ('00ffff', (0.2247, 0.3287)),
     ('ff00ff', (0.3209, 0.1542)),
     ('800080', (0.3209, 0.1542))])
def test_Color_xy(
    source: str,
    expect: tuple[int, ...],
) -> None:
    """
    Perform various tests associated with relevant routines.

    :param source: Source color used when converting values.
    :param expect: Expected output from the testing routine.
    """

    assert Color(source).xy == expect



@mark.parametrize(
    'source,expect',
    [('ff00cc', (312, 100, 50)),
     ('ffffff', (0, 0, 100)),
     ('000000', (0, 0, 0)),
     ('ff0000', (0, 100, 50)),
     ('00ff00', (120, 100, 50)),
     ('0000ff', (240, 100, 50)),
     ('808080', (0, 0, 50)),
     ('ffff00', (60, 100, 50)),
     ('00ffff', (180, 100, 50)),
     ('ff00ff', (300, 100, 50)),
     ('800080', (300, 100, 25))])
def test_Color_hsl(
    source: str,
    expect: tuple[int, ...],
) -> None:
    """
    Perform various tests associated with relevant routines.

    :param source: Source color used when converting values.
    :param expect: Expected output from the testing routine.
    """

    assert Color(source).hsl == expect



def test_Color_cover() -> None:
    """
    Perform various tests associated with relevant routines.
    """

    color1 = Color('000001')
    color2 = Color('#000001')

    assert not (color1 > None)  # type: ignore
    assert not (color1 >= None)  # type: ignore
    assert not (color1 <= None)  # type: ignore
    assert not (color1 < None)  # type: ignore

    assert color1 - color2 == 0
    assert color1 - '000001' == 0
    assert color1 + color2 == 2
    assert color1 + '000001' == 2
