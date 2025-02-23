"""
Functions and routines associated with Enasis Network Common Library.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from datetime import datetime
from re import compile
from typing import TYPE_CHECKING
from typing import Union

if TYPE_CHECKING:
    from .time import Time



NUMERISH = compile(
    r'^\-?\d+(\.\d+)?$')

SNAPABLE = compile(
    r'^(\-|\+)[\d\@a-z\-\+]+$')

UNITIME = Union[
    int | float | str]

STRINGNOW = {
    'None', None,
    'null', 'now'}



NUMERIC = Union[int, float]

PARSABLE = Union[
    str, NUMERIC,
    datetime, 'Time']

SCHEDULE = Union[
    str, dict[str, int]]



UNIXEPOCH = (
    '1970-01-01T00:00:00+0000')

UNIXMPOCH = (
    '1970-01-01T00:00:00.000000+0000')

UNIXSPOCH = (
    '1970-01-01T00:00:00Z')

UNIXHPOCH = (
    '01/01/1970 12:00AM UTC')



STAMP_SIMPLE = (
    '%Y-%m-%dT%H:%M:%S%z')

STAMP_SUBSEC = (
    '%Y-%m-%dT%H:%M:%S.%f%z')

STAMP_HUMAN = (
    '%m/%d/%Y %I:%M%p %Z')
