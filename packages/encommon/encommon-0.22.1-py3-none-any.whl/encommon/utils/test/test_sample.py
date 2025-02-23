"""
Functions and routines associated with Enasis Network Common Library.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from copy import deepcopy
from json import dumps
from json import loads
from pathlib import Path

from ..sample import load_sample
from ..sample import prep_sample
from ..sample import read_sample
from ..sample import rvrt_sample
from ..stdout import ArrayColors
from ... import PROJECT
from ...config import LoggerParams
from ...utils.sample import ENPYRWS



_PREFIX = 'encommon_sample'

_SOURCE = {
    'list': ['bar', 'baz'],
    'tuple': (1, 2),
    'project': PROJECT,
    'other': '/pat/h',
    'devnull': '/dev/null'}

_EXPECT = {
    'list': ['bar', 'baz'],
    'tuple': [1, 2],
    'project': f'_/{_PREFIX}/PROJECT/_',
    'other': f'_/{_PREFIX}/pytemp/_',
    'devnull': '/dev/null'}

_REPLACES = {
    'PROJECT': str(PROJECT),
    'pytemp': '/pat/h'}



def test_prep_sample() -> None:
    """
    Perform various tests associated with relevant routines.
    """

    colors = ArrayColors()

    params = LoggerParams()

    source = {
        'colors': colors,
        'params': params}

    sample = prep_sample(
        content=source,
        indent=None)

    assert loads(sample) == {
        'colors': {
            'bool': 93,
            'colon': 37,
            'empty': 36,
            'hyphen': 37,
            'key': 97,
            'label': 37,
            'none': 33,
            'num': 93,
            'other': 91,
            'str': 92,
            'times': 96},
        'params': {
            'file_level': None,
            'file_path': None,
            'stdo_level': None}}



def test_load_sample(
    tmp_path: Path,
) -> None:
    """
    Perform various tests associated with relevant routines.

    :param tmp_path: pytest object for temporal filesystem.
    """

    source = deepcopy(_SOURCE)

    expect = deepcopy(_EXPECT)


    sample_path = (
        tmp_path / 'samples.json')

    sample = load_sample(
        path=sample_path,
        update=ENPYRWS,
        content=source,
        replace=_REPLACES)

    _expect = dumps(
        expect, indent=2)

    assert _expect == sample


    source |= {'list': [1, 3, 2]}
    expect |= {'list': [1, 3, 2]}

    sample = load_sample(
        path=sample_path,
        content=source,
        update=True,
        replace=_REPLACES)

    _expect = dumps(
        expect, indent=2)

    assert _expect == sample



def test_read_sample(
    tmp_path: Path,
) -> None:
    """
    Perform various tests associated with relevant routines.

    :param tmp_path: pytest object for temporal filesystem.
    """

    source = prep_sample(
        content=_SOURCE,
        indent=None)

    sample = read_sample(
        sample=source,
        replace=_REPLACES)

    sample = prep_sample(
        content=loads(sample),
        replace=_REPLACES,
        indent=None)

    expect = dumps(_EXPECT)

    assert expect == sample



def test_rvrt_sample(
    tmp_path: Path,
) -> None:
    """
    Perform various tests associated with relevant routines.

    :param tmp_path: pytest object for temporal filesystem.
    """

    source = prep_sample(
        content=_SOURCE,
        indent=None)

    sample = rvrt_sample(
        sample=source,
        replace=_REPLACES)

    sample = prep_sample(
        content=loads(sample),
        replace=_REPLACES,
        indent=None)

    expect = dumps(_EXPECT)

    assert expect == sample
