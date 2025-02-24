"""
Functions and routines associated with Enasis Network Common Library.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from pathlib import Path
from time import sleep

from pytest import fixture
from pytest import raises

from ..params import WindowParams
from ..params import WindowsParams
from ..windows import Windows
from ..windows import WindowsTable
from ...types import DictStrAny
from ...types import inrepr
from ...types import instr
from ...types import lattrs



@fixture
def windows(
    tmp_path: Path,
) -> Windows:
    """
    Construct the instance for use in the downstream tests.

    :param tmp_path: pytest object for temporal filesystem.
    :returns: Newly constructed instance of related class.
    """


    source: DictStrAny = {
        'one': WindowParams(
            window='* * * * *',
            start=310,
            stop=610,
            delay=10),
        'two': WindowParams(
            window='* * * * *',
            start=300,
            stop=620,
            delay=10)}


    params = WindowsParams(
        windows=source)

    store = (
        f'sqlite:///{tmp_path}'
        '/cache.db')

    windows = Windows(
        params,
        start=310,
        stop=610,
        store=store)

    session = windows.store_session


    window = WindowsTable(
        group='default',
        unique='two',
        last='1970-01-01T00:06:00Z',
        next='1970-01-01T00:07:00Z',
        update='1970-01-01T01:00:00Z')

    session.add(window)

    session.commit()


    window = WindowsTable(
        group='default',
        unique='tre',
        last='1970-01-01T00:06:00Z',
        next='1970-01-01T00:07:00Z',
        update='1970-01-01T01:00:00Z')

    session.add(window)

    session.commit()


    windows.load_children()

    return windows



def test_Windows(
    windows: 'Windows',
) -> None:
    """
    Perform various tests associated with relevant routines.

    :param windows: Primary class instance for window object.
    """


    attrs = lattrs(windows)

    assert attrs == [
        '_Windows__params',
        '_Windows__store',
        '_Windows__group',
        '_Windows__store_engine',
        '_Windows__store_session',
        '_Windows__start',
        '_Windows__stop',
        '_Windows__windows']


    assert inrepr(
        'windows.Windows object',
        windows)

    assert isinstance(
        hash(windows), int)

    assert instr(
        'windows.Windows object',
        windows)


    assert windows.params

    assert windows.store[:6] == 'sqlite'

    assert windows.group == 'default'

    assert windows.store_engine

    assert windows.store_session

    assert windows.start == (
        '1970-01-01T00:05:10Z')

    assert windows.stop == (
        '1970-01-01T00:10:10Z')

    assert len(windows.children) == 2


    window = windows.children['one']

    assert window.next == (
        '1970-01-01T00:06:00Z')

    assert window.last == (
        '1970-01-01T00:05:00Z')


    window = windows.children['two']

    assert window.next == (
        '1970-01-01T00:08:00Z')

    assert window.last == (
        '1970-01-01T00:07:00Z')



def test_Windows_cover(
    windows: 'Windows',
) -> None:
    """
    Perform various tests associated with relevant routines.

    :param windows: Primary class instance for window object.
    """


    assert windows.ready('two')

    windows.update('two', '+1h')

    assert not windows.ready('two')


    windows = Windows()

    params = WindowParams(window=1)

    windows.create('fur', params)

    assert not windows.ready('fur')

    sleep(2)

    assert windows.ready('fur')

    windows.delete('fur')



def test_Windows_raises(
    windows: Windows,
) -> None:
    """
    Perform various tests associated with relevant routines.

    :param windows: Primary class instance for window object.
    """


    _raises = raises(ValueError)

    with _raises as reason:
        windows.ready('dne')

    _reason = str(reason.value)

    assert _reason == 'unique'


    _raises = raises(ValueError)

    params = WindowParams(
        window='* * * * *')

    with _raises as reason:
        windows.create('one', params)

    _reason = str(reason.value)

    assert _reason == 'unique'


    _raises = raises(ValueError)

    with _raises as reason:
        windows.update('dne', 'now')

    _reason = str(reason.value)

    assert _reason == 'unique'
