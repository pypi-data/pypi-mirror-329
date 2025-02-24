"""
Functions and routines associated with Enasis Network Common Library.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from typing import TYPE_CHECKING

from ...types import inrepr
from ...types import instr
from ...types import lattrs

if TYPE_CHECKING:
    from ..content import Content



def test_Content(
    content: 'Content',
) -> None:
    """
    Perform various tests associated with relevant routines.

    :param content: Primary class instance for the content.
    """


    attrs = lattrs(content)

    assert attrs == []


    assert inrepr(
        'content.Content',
        content)

    assert isinstance(
        hash(content), int)

    assert instr(
        'content.Content',
        content)


    script = (
        content
        .scripts('default'))

    assert script is not None


    styles = (
        content
        .styles('default'))

    assert styles is not None


    image = (
        content
        .images('enasis'))

    assert image is not None



def test_Content_cover(
    content: 'Content',
) -> None:
    """
    Perform various tests associated with relevant routines.

    :param content: Primary class instance for the content.
    """


    script = (
        content
        .scripts('doesnotexist'))

    assert script is None


    styles = (
        content
        .styles('doesnotexist'))

    assert styles is None


    image = (
        content
        .images('doesnotexist'))

    assert image is None
