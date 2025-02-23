"""
Functions and routines associated with Enasis Network Common Library.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from pathlib import Path
from typing import Optional

from ..utils import read_text



IMAGES = (
    Path(__file__).parent
    / 'images')

SCRIPTS = (
    Path(__file__).parent
    / 'scripts')

STYLES = (
    Path(__file__).parent
    / 'styles')



class Content:
    """
    Access common content used with application interfaces.
    """


    @classmethod
    def images(
        cls,
        name: str,
    ) -> Optional[str]:
        """
        Return the contents requested stored within the project.

        :param name: Which file in the project will be returned.
        :returns: Contents requested stored within the project.
        """

        path = IMAGES / f'{name}.svg'

        if not path.exists():
            return None

        return read_text(path)


    @classmethod
    def scripts(
        cls,
        name: str,
    ) -> Optional[str]:
        """
        Return the contents requested stored within the project.

        :param name: Which file in the project will be returned.
        :returns: Contents requested stored within the project.
        """

        path = SCRIPTS / f'{name}.js'

        if not path.exists():
            return None

        return read_text(path)


    @classmethod
    def styles(
        cls,
        name: str,
    ) -> Optional[str]:
        """
        Return the contents requested stored within the project.

        :param name: Which file in the project will be returned.
        :returns: Contents requested stored within the project.
        """

        path = STYLES / f'{name}.css'

        if not path.exists():
            return None

        return read_text(path)
