"""
Functions and routines associated with Enasis Network Common Library.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from contextlib import suppress
from typing import Union

from ..types import strplwr



class Color:
    """
    Covert colors to various forms using provided hex value.

    Example
    -------
    >>> color = Color('#003333')
    >>> color.rgb
    (0, 51, 51)
    >>> color.hsl
    (180, 100, 10)
    >>> color.xyz
    (1.7814, 2.6067, 3.5412)
    >>> color.xy
    (0.2247, 0.3287)

    Example
    -------
    >>> color1 = Color('#003333')
    >>> color2 = Color('#330000')
    >>> color1 - color2
    Color('#32CCCD')
    >>> color1 + color2
    Color('#333333')

    :param source: Source color used when converting values.
    """

    __source: str


    def __init__(
        self,
        source: str,
    ) -> None:
        """
        Initialize instance for class using provided parameters.
        """

        if source[:1] == '#':
            source = source[1:]

        source = strplwr(source)

        self.__source = source


    def __repr__(
        self,
    ) -> str:
        """
        Built-in method for representing the values for instance.

        :returns: String representation for values from instance.
        """

        color = self.__str__()

        return f"Color('{color}')"


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

        color = self.__source.upper()

        return f'#{color}'


    def __int__(
        self,
    ) -> int:
        """
        Built-in method representing numeric value for instance.

        :returns: Numeric representation for value in instance.
        """

        return int(self.__source, 16)


    def __float__(
        self,
    ) -> float:
        """
        Built-in method representing numeric value for instance.

        :returns: Numeric representation for value in instance.
        """

        return float(self.__int__())


    def __add__(
        self,
        other: Union[int, str, 'Color'],
    ) -> 'Color':
        """
        Built-in method for mathematically processing the value.

        :param other: Other value being compared with instance.
        :returns: Python timedelta object containing the answer.
        """

        if isinstance(other, str):
            other = Color(other)

        source = self.__int__()
        _source = int(other)

        outcome = abs(source + _source)

        result = f'{outcome:06x}'

        return Color(result)


    def __sub__(
        self,
        other: Union[int, str, 'Color'],
    ) -> 'Color':
        """
        Built-in method for mathematically processing the value.

        :param other: Other value being compared with instance.
        :returns: Python timedelta object containing the answer.
        """

        if isinstance(other, str):
            other = Color(other)

        source = self.__int__()
        _source = int(other)

        outcome = abs(source - _source)

        result = f'{outcome:06x}'

        return Color(result)


    def __eq__(
        self,
        other: object,
    ) -> bool:
        """
        Built-in method for comparing this instance with another.

        :param other: Other value being compared with instance.
        :returns: Boolean indicating outcome from the operation.
        """

        with suppress(Exception):

            if isinstance(other, int):
                other = f'{other:06x}'

            if isinstance(other, str):
                other = Color(other)

            assert hasattr(
                other, 'source')

            source = self.__source
            _source = other.source

            assert isinstance(_source, str)

            return source == _source

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
        other: Union[int, str, 'Color'],
    ) -> bool:
        """
        Built-in method for comparing this instance with another.

        :param other: Other value being compared with instance.
        :returns: Boolean indicating outcome from the operation.
        """

        with suppress(Exception):

            if isinstance(other, int):
                other = f'{other:06x}'

            if isinstance(other, str):
                other = Color(other)

            assert hasattr(
                other, 'source')

            source = self.__source
            _source = other.source

            assert isinstance(_source, str)

            return source > _source

        return False


    def __ge__(
        self,
        other: Union[int, str, 'Color'],
    ) -> bool:
        """
        Built-in method for comparing this instance with another.

        :param other: Other value being compared with instance.
        :returns: Boolean indicating outcome from the operation.
        """

        with suppress(Exception):

            if isinstance(other, int):
                other = f'{other:06x}'

            if isinstance(other, str):
                other = Color(other)

            assert hasattr(
                other, 'source')

            source = self.__source
            _source = other.source

            assert isinstance(_source, str)

            return source >= _source

        return False


    def __lt__(
        self,
        other: Union[int, str, 'Color'],
    ) -> bool:
        """
        Built-in method for comparing this instance with another.

        :param other: Other value being compared with instance.
        :returns: Boolean indicating outcome from the operation.
        """

        with suppress(Exception):

            if isinstance(other, int):
                other = f'{other:06x}'

            if isinstance(other, str):
                other = Color(other)

            assert hasattr(
                other, 'source')

            source = self.__source
            _source = other.source

            assert isinstance(_source, str)

            return source < _source

        return False


    def __le__(
        self,
        other: Union[int, str, 'Color'],
    ) -> bool:
        """
        Built-in method for comparing this instance with another.

        :param other: Other value being compared with instance.
        :returns: Boolean indicating outcome from the operation.
        """

        with suppress(Exception):

            if isinstance(other, int):
                other = f'{other:06x}'

            if isinstance(other, str):
                other = Color(other)

            assert hasattr(
                other, 'source')

            source = self.__source
            _source = other.source

            assert isinstance(_source, str)

            return source <= _source

        return False


    @property
    def source(
        self,
    ) -> str:
        """
        Return the value for the attribute from class instance.

        :returns: Value for the attribute from class instance.
        """

        return self.__source


    @property
    def rgb(
        self,
    ) -> tuple[int, int, int]:
        """
        Return the value for the attribute from class instance.

        :returns: Value for the attribute from class instance.
        """

        color = self.__source

        return (
            int(color[0:2], 16),
            int(color[2:4], 16),
            int(color[4:6], 16))


    @property
    def xyz(
        self,
    ) -> tuple[float, float, float]:
        """
        Return the value for the attribute from class instance.

        :returns: Value for the attribute from class instance.
        """

        _red, _grn, _blu = self.rgb

        red = _red / 255.0
        grn = _grn / 255.0
        blu = _blu / 255.0

        if red > 0.04045:
            red += 0.055
            red /= 1.055
            red **= 2.4

        else:
            red = red / 12.92

        if grn > 0.04045:
            grn += 0.055
            grn /= 1.055
            grn **= 2.4

        else:
            grn = grn / 12.92

        if blu > 0.04045:
            blu += 0.055
            blu /= 1.055
            blu **= 2.4

        else:
            blu = blu / 12.92

        red = red * 100
        grn = grn * 100
        blu = blu * 100

        x = (
            red * 0.4124
            + grn * 0.3576
            + blu * 0.1805)

        y = (
            red * 0.2126
            + grn * 0.7152
            + blu * 0.0722)

        z = (
            red * 0.0193
            + grn * 0.1192
            + blu * 0.9505)

        x = round(x, 4)
        y = round(y, 4)
        z = round(z, 4)

        return x, y, z


    @property
    def xy(
        self,
    ) -> tuple[float, float]:
        """
        Return the value for the attribute from class instance.

        :returns: Value for the attribute from class instance.
        """

        x, y, z = self.xyz

        if x + y + z == 0:
            return 0, 0

        cx = x / (x + y + z)
        cy = y / (x + y + z)

        cx = round(cx, 4)
        cy = round(cy, 4)

        return cx, cy


    @property
    def hsl(
        self,
    ) -> tuple[int, int, int]:
        """
        Return the value for the attribute from class instance.

        :returns: Value for the attribute from class instance.
        """

        _red, _grn, _blu = self.rgb

        red = _red / 255
        grn = _grn / 255
        blu = _blu / 255

        mam = max(red, grn, blu)
        mim = min(red, grn, blu)

        hue = sat = 0.0
        lev = (mam + mim) / 2

        if mam != mim:

            delta = mam - mim

            sat = (
                delta / (2 - mam - mim)
                if lev > 0.5
                else delta / (mam + mim))

            if mam == red:
                hue = (grn - blu) / delta
                hue += 6 if grn < blu else 0

            elif mam == grn:
                hue = (blu - red) / delta
                hue += 2

            elif mam == blu:
                hue = (red - grn) / delta
                hue += 4

            hue /= 6

        hue = int(hue * 360)
        sat = int(sat * 100)
        lev = int(lev * 100)

        return hue, sat, lev
