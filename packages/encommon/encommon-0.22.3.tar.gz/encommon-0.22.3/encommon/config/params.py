"""
Functions and routines associated with Enasis Network Common Library.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from pathlib import Path
from typing import Annotated
from typing import Any
from typing import Optional

from pydantic import Field

from .logger import LOGLEVELS
from ..crypts import CryptsParams
from ..types import BaseModel



class ConfigParams(BaseModel, extra='forbid'):
    """
    Process and validate the core configuration parameters.
    """

    paths: Annotated[
        Optional[list[str]],
        Field(None,
              description='Location of configuration files',
              min_length=1)]



class LoggerParams(BaseModel, extra='forbid'):
    """
    Process and validate the core configuration parameters.
    """

    stdo_level: Annotated[
        Optional[LOGLEVELS],
        Field(None,
              description='Minimum logging message level',
              min_length=1)]

    file_level: Annotated[
        Optional[LOGLEVELS],
        Field(None,
              description='Minimum logging message level',
              min_length=1)]

    file_path: Annotated[
        Optional[str],
        Field(None,
              description='Enable output to the log file',
              min_length=1)]


    def __init__(
        self,
        /,
        **data: Any,
    ) -> None:
        """
        Initialize instance for class using provided parameters.
        """

        file_path = data.get('file_path')

        if isinstance(file_path, Path):
            data['file_path'] = str(file_path)

        super().__init__(**data)



class Params(BaseModel, extra='forbid'):
    """
    Process and validate the core configuration parameters.
    """

    enconfig: Annotated[
        Optional[ConfigParams],
        Field(None,
              description='Parameters for Config instance')]

    enlogger: Annotated[
        Optional[LoggerParams],
        Field(None,
              description='Parameters for Logger instance')]

    encrypts: Annotated[
        Optional[CryptsParams],
        Field(None,
              description='Parameters for Crypts instance')]
