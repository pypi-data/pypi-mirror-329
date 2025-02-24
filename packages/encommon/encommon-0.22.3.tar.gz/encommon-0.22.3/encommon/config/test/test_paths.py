"""
Functions and routines associated with Enasis Network Common Library.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from pathlib import Path

from pytest import fixture

from . import SAMPLES
from ..paths import ConfigPath
from ..paths import ConfigPaths
from ... import PROJECT
from ...types import inrepr
from ...types import instr
from ...types import lattrs
from ...utils import load_sample
from ...utils import prep_sample
from ...utils.sample import ENPYRWS



@fixture
def paths(
    config_path: Path,
) -> ConfigPaths:
    """
    Construct the instance for use in the downstream tests.

    :param config_path: Custom fixture for populating paths.
    :returns: Newly constructed instance of related class.
    """

    return ConfigPaths([
        f'{SAMPLES}/stark',
        f'{SAMPLES}/wayne'])



def test_ConfigPath(
    config_path: Path,
) -> None:
    """
    Perform various tests associated with relevant routines.

    :param config_path: Custom fixture for populating paths.
    """

    path = ConfigPath(config_path)


    attrs = lattrs(path)

    assert attrs == [
        'path',
        'config']


    assert inrepr(
        'paths.ConfigPath object',
        path)

    assert isinstance(
        hash(path), int)

    assert instr(
        'paths.ConfigPath object',
        path)


    assert 'test' in path.path.name

    assert len(path.config) == 1



def test_ConfigPaths(
    paths: ConfigPaths,
) -> None:
    """
    Perform various tests associated with relevant routines.

    :param paths: Custom fixture for the configuration paths.
    """


    attrs = lattrs(paths)

    assert attrs == [
        'paths', 'config',
        '_ConfigPaths__merge']


    assert inrepr(
        'paths.ConfigPaths object',
        paths)

    assert isinstance(
        hash(paths), int)

    assert instr(
        'paths.ConfigPaths object',
        paths)


    assert len(paths.paths) == 2

    assert len(paths.config) == 2


    replaces = {
        'PROJECT': PROJECT}

    sample_path = (
        SAMPLES / 'paths.json')

    sample = load_sample(
        path=sample_path,
        update=ENPYRWS,
        content=paths.merge,
        replace=replaces)

    expect = prep_sample(
        content=paths.merge,
        replace=replaces)

    assert expect == sample



def test_ConfigPaths_cover(
    paths: ConfigPaths,
) -> None:
    """
    Perform various tests associated with relevant routines.

    :param paths: Custom fixture for the configuration paths.
    """

    merge1 = paths.merge
    merge2 = paths.merge

    assert merge1 is not merge2
