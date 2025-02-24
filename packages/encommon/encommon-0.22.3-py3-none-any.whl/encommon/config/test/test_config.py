"""
Functions and routines associated with Enasis Network Common Library.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from pathlib import Path
from typing import TYPE_CHECKING

from . import SAMPLES
from ... import PROJECT
from ...types import inrepr
from ...types import instr
from ...types import lattrs
from ...utils import load_sample
from ...utils import prep_sample
from ...utils.sample import ENPYRWS

if TYPE_CHECKING:
    from ..config import Config



def test_Config(
    tmp_path: Path,
    config: 'Config',
) -> None:
    """
    Perform various tests associated with relevant routines.

    :param tmp_path: pytest object for temporal filesystem.
    :param config: Primary class instance for configuration.
    """


    attrs = lattrs(config)

    assert attrs == [
        '_Config__model',
        '_Config__files',
        '_Config__cargs',
        '_Config__sargs',
        '_Config__params',
        '_Config__paths',
        '_Config__logger',
        '_Config__crypts']


    assert inrepr(
        'config.Config object',
        config)

    assert isinstance(
        hash(config), int)

    assert instr(
        'config.Config object',
        config)


    assert config.files.merge

    assert config.paths.merge

    assert len(config.cargs) == 1

    assert len(config.sargs) == 1

    assert len(config.basic) == 3

    assert len(config.merge) == 5

    assert callable(config.model)

    assert config.params

    assert len(config.config) == 3

    assert config.logger

    assert config.crypts


    replaces = {
        'pytemp': tmp_path,
        'PROJECT': PROJECT}


    sample_path = (
        SAMPLES / 'basic.json')

    sample = load_sample(
        path=sample_path,
        update=ENPYRWS,
        content=config.basic,
        replace=replaces)

    expect = prep_sample(
        content=config.basic,
        replace=replaces)

    assert expect == sample


    sample_path = (
        SAMPLES / 'merge.json')

    sample = load_sample(
        path=sample_path,
        update=ENPYRWS,
        content=config.merge,
        replace=replaces)

    expect = prep_sample(
        content=config.merge,
        replace=replaces)

    assert expect == sample


    sample_path = (
        SAMPLES / 'config.json')

    sample = load_sample(
        path=sample_path,
        update=ENPYRWS,
        content=config.config,
        replace=replaces)

    expect = prep_sample(
        content=config.config,
        replace=replaces)

    assert expect == sample



def test_Config_cover(
    config: 'Config',
) -> None:
    """
    Perform various tests associated with relevant routines.

    :param config: Primary class instance for configuration.
    """


    logger1 = config.logger
    logger2 = config.logger

    assert logger1 is logger2


    crypts1 = config.crypts
    crypts2 = config.crypts

    assert crypts1 is crypts2
