"""
Functions and routines associated with Enasis Network Common Library.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from typing import TYPE_CHECKING

from ..classes import clsname
from ..classes import lattrs
from ...config import LoggerParams

if TYPE_CHECKING:
    from ...config import Config



def test_BaseModel() -> None:
    """
    Perform various tests associated with relevant routines.
    """

    params = LoggerParams(
        stdo_level='info')

    dumped = params.endumped
    pruned = params.enpruned

    assert dumped == {
        'file_level': None,
        'file_path': None,
        'stdo_level': 'info'}

    assert pruned == {
        'stdo_level': 'info'}



def test_clsname(
    config: 'Config',
) -> None:
    """
    Perform various tests associated with relevant routines.

    :param config: Primary class instance for configuration.
    """

    assert clsname(config) == 'Config'



def test_lattrs(
    config: 'Config',
) -> None:
    """
    Perform various tests associated with relevant routines.

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
