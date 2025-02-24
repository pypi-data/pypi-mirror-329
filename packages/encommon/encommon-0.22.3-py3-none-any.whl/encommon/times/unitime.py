"""
Functions and routines associated with Enasis Network Common Library.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from re import compile
from re import match as re_match

from .common import UNITIME
from .parse import since_time



NOTATE = compile(
    r'^(\d+(s|m|h|d|w|y))*$')

STRINT = compile(
    r'^\d+$')

STRFLT = compile(
    r'^\d+\.\d+$')



def unitime(
    input: UNITIME,
) -> int:
    """
    Return the seconds in integer format for provided input.

    Example
    -------
    >>> unitime('1d')
    86400
    >>> unitime('1y')
    31536000
    >>> unitime('1w3d4h')
    878400

    :param input: Input that will be converted into seconds.
    :returns: Seconds in integer format for provided input.
    """

    if isinstance(input, str):

        if re_match(STRINT, input):
            input = int(input)

        elif re_match(STRFLT, input):
            input = int(
                input.split('.')[0])

        elif re_match(NOTATE, input):
            input = since_time(
                'now', f'+{input}')

        else:  # NOCVR
            raise ValueError('input')

    if isinstance(input, float):
        input = int(input)

    assert isinstance(input, int)

    return input
