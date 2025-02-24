"""
Functions and routines associated with Enasis Network Common Library.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from typing import Annotated
from typing import Optional

from pydantic import Field

from ..types import BaseModel



_CRYPTS = dict[str, 'CryptParams']



class CryptParams(BaseModel, extra='forbid'):
    """
    Process and validate the core configuration parameters.
    """

    phrase: Annotated[
        str,
        Field(...,
              description='Passphrase for the operations',
              min_length=1)]


    def __init__(
        self,
        phrase: str,
    ) -> None:
        """
        Initialize instance for class using provided parameters.
        """

        super().__init__(**{
            'phrase': phrase})



class CryptsParams(BaseModel, extra='forbid'):
    """
    Process and validate the core configuration parameters.
    """

    phrases: Annotated[
        _CRYPTS,
        Field(...,
              description='Passphrases for the operations',
              min_length=0)]


    def __init__(
        self,
        phrases: Optional[_CRYPTS] = None,
    ) -> None:
        """
        Initialize instance for class using provided parameters.
        """

        phrases = phrases or {}

        super().__init__(**{
            'phrases': phrases})
