"""
Functions and routines associated with Enasis Network Common Library.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from pathlib import Path

from pytest import fixture

from .config import Config
from .config.test import SAMPLES
from .utils import save_text



def config_factory(
    tmp_path: Path,
) -> Config:
    """
    Construct the instance for use in the downstream tests.

    :param tmp_path: pytest object for temporal filesystem.
    :returns: Newly constructed instance of related class.
    """

    content = (
        f"""

        enconfig:
          paths:
            - '{SAMPLES}/stark'
            - '{SAMPLES}/wayne'

        enlogger:
          stdo_level: debug

        encrypts:
          phrases:
            default:
              phrase: phrase

        """)

    config_path = (
        tmp_path / 'config.yml')

    config_log = (
        tmp_path / 'config.log')

    save_text(
        config_path, content)

    logger = {
        'file_path': config_log,
        'file_level': 'info'}

    cargs = {'enlogger': logger}
    sargs = {'cus/tom': 'fart'}

    return Config(
        config_path,
        cargs=cargs,
        sargs=sargs)



@fixture
def config_path(
    tmp_path: Path,
) -> Path:
    """
    Construct the directory and files needed for the tests.

    :param tmp_path: pytest object for temporal filesystem.
    :returns: New resolved filesystem path object instance.
    """

    config_factory(tmp_path)

    return tmp_path.resolve()



@fixture
def config(
    tmp_path: Path,
) -> Config:
    """
    Construct the instance for use in the downstream tests.

    :param tmp_path: pytest object for temporal filesystem.
    :returns: Newly constructed instance of related class.
    """

    return config_factory(tmp_path)
