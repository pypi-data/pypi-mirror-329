"""
Functions and routines associated with Enasis Network Common Library.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from copy import deepcopy
from pathlib import Path



SAMPLES = (
    Path(__file__).parent
    / 'samples')



_DICT1 = {
    'dict1': 'dict1',
    'str': 'd1string',
    'list': ['d1list'],
    'tuple': (1, 2),
    'dict': {'key': 'd1dict'},
    'bool': False,
    'null': None}

_DICT2 = {
    'dict2': 'dict2',
    'str': 'd2string',
    'list': ['d2list'],
    'tuple': (3, 4),
    'dict': {'key': 'd2dict'},
    'bool': True,
    'null': 'null'}

_DICT1R = deepcopy(_DICT1)
_DICT2R = deepcopy(_DICT2)

_DICT1R['recurse'] = (
    deepcopy(_DICT1))

_DICT2R['recurse'] = (
    deepcopy(_DICT2))

_DICT1R['nested'] = [
    deepcopy(_DICT1)]

_DICT2R['nested'] = [
    deepcopy(_DICT2)]
