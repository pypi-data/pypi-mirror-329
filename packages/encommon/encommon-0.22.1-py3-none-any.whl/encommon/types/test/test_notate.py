"""
Functions and routines associated with Enasis Network Common Library.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from copy import deepcopy
from pathlib import Path

from _pytest.python_api import RaisesContext

from pytest import fixture
from pytest import raises

from . import SAMPLES
from . import _DICT1R
from ..notate import delate
from ..notate import expate
from ..notate import getate
from ..notate import impate
from ..notate import setate
from ..types import DictStrAny
from ...utils import load_sample
from ...utils import prep_sample
from ...utils.sample import ENPYRWS



_SAMPLE = dict[str, DictStrAny]



@fixture
def sample_impate() -> _SAMPLE:
    """
    Construct the dictionary for use with downstream tests.

    :returns: Newly constructed dictionary for use in tests.
    """

    recurse_implode = (
        impate(
            deepcopy(_DICT1R),
            recurse_list=True,
            implode_list=True))

    assert isinstance(
        recurse_implode, dict)

    nocurse_noplode = (
        impate(
            deepcopy(_DICT1R),
            recurse_list=False,
            implode_list=False))

    assert isinstance(
        nocurse_noplode, dict)

    recurse_noplode = (
        impate(
            deepcopy(_DICT1R),
            recurse_list=True,
            implode_list=False))

    assert isinstance(
        recurse_noplode, dict)

    nocurse_implode = (
        impate(
            deepcopy(_DICT1R),
            recurse_list=False,
            implode_list=True))

    assert isinstance(
        nocurse_implode, dict)


    return {
        'recurse_implode': recurse_implode,
        'nocurse_noplode': nocurse_noplode,
        'recurse_noplode': recurse_noplode,
        'nocurse_implode': nocurse_implode}



@fixture
def sample_expate(
    sample_impate: _SAMPLE,
) -> _SAMPLE:
    """
    Construct the dictionary for use with downstream tests.

    :param sample_impate: Source dictionary for use in test.
    :returns: Newly constructed dictionary for use in tests.
    """

    recurse_implode = (
        sample_impate[
            'recurse_implode'])

    assert isinstance(
        recurse_implode, dict)

    nocurse_noplode = (
        sample_impate[
            'nocurse_noplode'])

    assert isinstance(
        nocurse_noplode, dict)

    recurse_noplode = (
        sample_impate[
            'recurse_noplode'])

    assert isinstance(
        recurse_noplode, dict)

    nocurse_implode = (
        sample_impate[
            'nocurse_implode'])

    assert isinstance(
        nocurse_implode, dict)

    return {
        'recurse_implode': (
            expate(recurse_implode)),
        'nocurse_noplode': (
            expate(nocurse_noplode)),
        'recurse_noplode': (
            expate(recurse_noplode)),
        'nocurse_implode': (
            expate(nocurse_implode))}



def test_getate() -> None:
    """
    Perform various tests associated with relevant routines.
    """

    source = deepcopy(_DICT1R)


    value = getate(['1', 2], '1')
    assert value == 2

    value = getate((1, 2), '1')
    assert value == 2

    value = getate({'1': 2}, '1')
    assert value == 2


    path = 'recurse/dict/key'
    value = getate(source, path)

    assert value == 'd1dict'


    path = 'recurse/list/0'
    value = getate(source, path)

    assert value == 'd1list'



def test_getate_cover() -> None:
    """
    Perform various tests associated with relevant routines.
    """

    source = deepcopy(_DICT1R)


    assert not getate({}, 'd/n/e')
    assert not getate([], '0/n/e')


    path = 'recurse/str/a'
    value = getate(source, path)

    assert value is None



def test_setate() -> None:
    """
    Perform various tests associated with relevant routines.
    """

    source = deepcopy(_DICT1R)


    path = 'list/1'
    before = getate(source, path)
    setate(source, path, 1)
    after = getate(source, path)
    assert after == 1
    assert before is None


    path = 'recurse/dict/key'
    before = getate(source, path)
    setate(source, path, 1)
    after = getate(source, path)
    assert after == 1
    assert before == 'd1dict'


    path = 'nested/0/dict/key'
    before = getate(source, path)
    setate(source, path, 1)
    after = getate(source, path)
    assert after == 1
    assert before == 'd1dict'


    path = 'recurse/list/0'
    before = getate(source, path)
    setate(source, path, 1)
    after = getate(source, path)
    assert after == 1
    assert before == 'd1list'



def test_setate_cover() -> None:
    """
    Perform various tests associated with relevant routines.
    """

    source = deepcopy(_DICT1R)


    path = 'nested/1/dict/key'
    before = getate(source, path)
    setate(source, path, 1)
    after = getate(source, path)
    assert after == 1
    assert before is None



def test_setate_raises() -> None:
    """
    Perform various tests associated with relevant routines.
    """

    _raises: RaisesContext[
        ValueError | IndexError]


    _raises = raises(ValueError)

    with _raises as reason:
        setate(1, '1', 1)  # type: ignore

    _reason = str(reason.value)

    assert _reason == 'source'


    _raises = raises(IndexError)

    with _raises as reason:
        setate([], '1', 1)

    _reason = str(reason.value)

    assert _reason == '1'



def test_delate() -> None:
    """
    Perform various tests associated with relevant routines.
    """

    source = deepcopy(_DICT1R)


    path = 'recurse/dict/key'
    before = getate(source, path)
    delate(source, path)
    after = getate(source, path)
    assert after is None
    assert before == 'd1dict'


    path = 'nested/0/dict/key'
    before = getate(source, path)
    delate(source, path)
    after = getate(source, path)
    assert after is None
    assert before == 'd1dict'


    path = 'recurse/list/0'
    before = getate(source, path)
    delate(source, path)
    after = getate(source, path)
    assert after is None
    assert before == 'd1list'



def test_delate_raises() -> None:
    """
    Perform various tests associated with relevant routines.
    """


    _raises = raises(ValueError)

    with _raises as reason:
        delate(1, '1')  # type: ignore

    _reason = str(reason.value)

    assert _reason == 'source'


    _raises = raises(ValueError)

    with _raises as reason:
        delate({'a': 1}, 'a/1/c')

    _reason = str(reason.value)

    assert _reason == 'source'



def test_impate(
    tmp_path: Path,
    sample_impate: _SAMPLE,
    sample_expate: _SAMPLE,
) -> None:
    """
    Perform various tests associated with relevant routines.

    :param sample_impate: Source dictionary for use in test.
    :param sample_expate: Source dictionary for use in test.
    :param tmp_path: pytest object for temporal filesystem.
    """

    sample_path = (
        SAMPLES / 'impate.json')

    sample = load_sample(
        path=sample_path,
        update=ENPYRWS,
        content=sample_impate)

    expect = prep_sample(
        content=sample_impate)

    assert expect == sample



def test_impate_cover(
    tmp_path: Path,
    sample_impate: _SAMPLE,
    sample_expate: _SAMPLE,
) -> None:
    """
    Perform various tests associated with relevant routines.

    :param sample_impate: Source dictionary for use in test.
    :param sample_expate: Source dictionary for use in test.
    :param tmp_path: pytest object for temporal filesystem.
    """


    default = sample_impate[
        'recurse_implode']

    assert default == impate(default)


    sample = 'recurse_noplode'

    implode = impate(
        [sample_expate[sample],
         sample_expate[sample]],
        implode_list=False,
        recurse_list=True)

    assert isinstance(implode, list)

    assert implode[0] == (
        sample_impate[sample])


    source = {'foo': {'bar': 'baz'}}
    expect = {'foo/bar': 'baz'}

    assert impate(source) == expect



def test_impate_raises() -> None:
    """
    Perform various tests associated with relevant routines.
    """

    _raises: RaisesContext[ValueError]


    _raises = raises(ValueError)

    with _raises as reason:
        impate('foo')  # type: ignore

    _reason = str(reason.value)

    assert _reason == 'source'



def test_expate(
    tmp_path: Path,
    sample_impate: _SAMPLE,
    sample_expate: _SAMPLE,
) -> None:
    """
    Perform various tests associated with relevant routines.

    :param sample_impate: Source dictionary for use in test.
    :param sample_expate: Source dictionary for use in test.
    :param tmp_path: pytest object for temporal filesystem.
    """

    sample_path = (
        SAMPLES / 'expate.json')

    sample = load_sample(
        path=sample_path,
        update=ENPYRWS,
        content=sample_expate)

    expect = prep_sample(
        content=sample_expate)

    assert expect == sample



def test_expate_cover(
    tmp_path: Path,
    sample_impate: _SAMPLE,
    sample_expate: _SAMPLE,
) -> None:
    """
    Perform various tests associated with relevant routines.

    :param sample_impate: Source dictionary for use in test.
    :param sample_expate: Source dictionary for use in test.
    :param tmp_path: pytest object for temporal filesystem.
    """


    assert sample_expate == (
        expate(sample_impate))


    assert sample_expate == (
        expate(sample_expate))


    assert all(
        x == _DICT1R for x in
        sample_expate.values())
