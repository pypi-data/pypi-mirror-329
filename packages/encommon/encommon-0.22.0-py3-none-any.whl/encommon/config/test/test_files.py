"""
Functions and routines associated with Enasis Network Common Library.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from pathlib import Path

from pytest import fixture

from . import SAMPLES
from ..files import ConfigFile
from ..files import ConfigFiles
from ...types import inrepr
from ...types import instr
from ...types import lattrs



@fixture
def files(
    config_path: Path,
) -> ConfigFiles:
    """
    Construct the instance for use in the downstream tests.

    :param config_path: Custom fixture for populating paths.
    :returns: Newly constructed instance of related class.
    """

    return ConfigFiles([
        f'{SAMPLES}/wayne/bwayne.yml',
        f'{SAMPLES}/stark/tstark.yml'])



def test_ConfigFile(
    config_path: Path,
) -> None:
    """
    Perform various tests associated with relevant routines.

    :param config_path: Custom fixture for populating paths.
    """

    file = ConfigFile(
        f'{config_path}/config.yml')


    attrs = lattrs(file)

    assert attrs == [
        'path',
        'config']


    assert inrepr(
        'files.ConfigFile object',
        file)

    assert isinstance(
        hash(file), int)

    assert instr(
        'files.ConfigFile object',
        file)


    assert file.path.name == 'config.yml'

    assert len(file.config) == 3



def test_ConfigFiles(
    files: ConfigFiles,
) -> None:
    """
    Perform various tests associated with relevant routines.

    :param files: Custom fixture for the configuration files.
    """


    attrs = lattrs(files)

    assert attrs == [
        'paths',
        'config',
        '_ConfigFiles__merge']


    assert inrepr(
        'files.ConfigFiles object',
        files)

    assert isinstance(
        hash(files), int)

    assert instr(
        'files.ConfigFiles object',
        files)


    assert len(files.paths) == 2

    assert len(files.config) == 2

    assert files.merge == {
        'name': 'Bruce Wayne'}



def test_ConfigFiles_cover(
    files: ConfigFiles,
) -> None:
    """
    Perform various tests associated with relevant routines.

    :param files: Custom fixture for the configuration files.
    """

    merge1 = files.merge
    merge2 = files.merge

    assert merge1 is not merge2
