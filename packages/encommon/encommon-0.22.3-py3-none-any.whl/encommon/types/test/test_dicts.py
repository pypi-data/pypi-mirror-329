"""
Functions and routines associated with Enasis Network Common Library.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from copy import deepcopy

from . import _DICT1
from . import _DICT1R
from . import _DICT2
from . import _DICT2R
from ..dicts import merge_dicts
from ..dicts import sort_dict



def test_merge_dicts() -> None:  # noqa: CFQ001
    """
    Perform various tests associated with relevant routines.
    """

    dict1 = deepcopy(_DICT1R)
    dict2 = deepcopy(_DICT2R)


    source = deepcopy(dict1)
    update = deepcopy(dict2)

    merge_dicts(source, update)

    assert source == {
        'dict1': 'dict1',
        'dict2': 'dict2',
        'str': 'd1string',
        'list': ['d1list', 'd2list'],
        'dict': {'key': 'd1dict'},
        'tuple': (1, 2),
        'bool': False,
        'null': None,
        'nested': [_DICT1, _DICT2],
        'recurse': {
            'dict1': 'dict1',
            'dict2': 'dict2',
            'str': 'd1string',
            'list': ['d1list', 'd2list'],
            'dict': {'key': 'd1dict'},
            'tuple': (1, 2),
            'bool': False,
            'null': None}}


    source = deepcopy(dict1)
    update = deepcopy(dict2)

    merge_dicts(source, update, True)

    assert source == {
        'dict1': 'dict1',
        'dict2': 'dict2',
        'str': 'd2string',
        'list': ['d1list', 'd2list'],
        'dict': {'key': 'd2dict'},
        'tuple': (3, 4),
        'bool': True,
        'null': 'null',
        'nested': [_DICT1, _DICT2],
        'recurse': {
            'dict1': 'dict1',
            'dict2': 'dict2',
            'str': 'd2string',
            'list': ['d1list', 'd2list'],
            'dict': {'key': 'd2dict'},
            'tuple': (3, 4),
            'bool': True,
            'null': 'null'}}


    source = deepcopy(dict1)
    update = deepcopy(dict2)

    merge_dicts(source, update, None)

    assert source == {
        'dict1': 'dict1',
        'dict2': 'dict2',
        'str': 'd1string',
        'list': ['d1list', 'd2list'],
        'dict': {'key': 'd1dict'},
        'tuple': (1, 2),
        'bool': False,
        'null': 'null',
        'nested': [_DICT1, _DICT2],
        'recurse': {
            'dict1': 'dict1',
            'dict2': 'dict2',
            'str': 'd1string',
            'list': ['d1list', 'd2list'],
            'dict': {'key': 'd1dict'},
            'tuple': (1, 2),
            'bool': False,
            'null': 'null'}}


    source = deepcopy(dict1)
    update = deepcopy(dict2)

    merge_dicts(
        source, update,
        merge_list=False,
        merge_dict=False)

    assert source == {
        'dict1': 'dict1',
        'dict2': 'dict2',
        'str': 'd1string',
        'list': ['d1list'],
        'dict': {'key': 'd1dict'},
        'tuple': (1, 2),
        'bool': False,
        'null': None,
        'nested': [_DICT1],
        'recurse': {
            'dict1': 'dict1',
            'str': 'd1string',
            'list': ['d1list'],
            'dict': {'key': 'd1dict'},
            'tuple': (1, 2),
            'bool': False,
            'null': None}}


    _source = merge_dicts(
        source, update,
        paranoid=True)

    assert source is not _source



def test_sort_dict() -> None:
    """
    Perform various tests associated with relevant routines.
    """

    assert sort_dict(_DICT1) == {
        'bool': False,
        'dict': {'key': 'd1dict'},
        'tuple': (1, 2),
        'dict1': 'dict1',
        'list': ['d1list'],
        'str': 'd1string',
        'null': None}
