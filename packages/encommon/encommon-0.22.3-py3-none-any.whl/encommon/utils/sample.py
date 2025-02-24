"""
Functions and routines associated with Enasis Network Common Library.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from dataclasses import asdict
from dataclasses import is_dataclass
from json import dumps
from os import environ
from pathlib import Path
from typing import Any
from typing import Callable
from typing import Optional


from .files import read_text
from .files import save_text
from ..types import BaseModel
from ..types import DictStrAny
from ..types import rplstr



PREFIX = 'encommon_sample'

ENPYRWS = (
    environ.get('ENPYRWS') == '1')



def prep_sample(  # noqa: CFQ004
    content: Any,
    *,
    default: Callable[[Any], str] = str,
    replace: Optional[DictStrAny] = None,
    indent: Optional[int] = 2,
) -> str:
    r"""
    Return the content after processing as the sample value.

    Example
    -------
    >>> prep_sample(['one', 'two'])
    '[\n  "one",\n  "two"\n]'

    Example
    -------
    >>> from ..types import Empty
    >>> prep_sample({'one': Empty})
    '{\n  "one": "Empty"\n}'

    :param content: Content that will be processed as JSON.
    :param default: Callable used when stringifying values.
    :param replace: Optional values to replace in the file.
    :returns: Content after processing as the sample value.
    """


    def _default(
        value: Any,  # noqa: ANN401
    ) -> DictStrAny | str:

        if is_dataclass(value):

            assert not isinstance(
                value, type)

            return asdict(value)

        if isinstance(value, BaseModel):
            return value.endumped

        return str(value)


    content = dumps(
        content,
        default=_default,
        indent=indent)

    replace = replace or {}

    items = replace.items()

    for old, new in items:

        new = str(new)

        old = f'_/{PREFIX}/{old}/_'

        content = rplstr(
            content, new, old)

    return str(content)



def load_sample(
    path: str | Path,
    content: Optional[Any] = None,
    update: bool = False,
    *,
    default: Callable[[Any], str] = str,
    replace: Optional[DictStrAny] = None,
) -> str:
    r"""
    Load the sample file and compare using provided content.

    .. testsetup::
       >>> from json import dumps
       >>> from json import loads
       >>> path = Path(getfixture('tmpdir'))
       >>> sample = path.joinpath('sample')

    Example
    -------
    >>> content = {'one': 'two'}
    >>> load_sample(sample, content)
    '{\n  "one": "two"\n}'

    Example
    -------
    >>> load_sample(sample)
    '{\n  "one": "two"\n}'

    :param path: Complete or relative path for sample file.
    :param update: Determine whether the sample is updated.
    :param content: Content that will be processed as JSON.
    :param default: Callable used when stringifying values.
    :param replace: Optional values to replace in the file.
    :returns: Content after processing using JSON functions.
    """


    path = Path(path).resolve()

    loaded: Optional[Any] = None


    content = prep_sample(
        content=content,
        default=default,
        replace=replace)


    def _save_sample() -> None:
        save_text(path, content)


    def _load_sample() -> str:
        return read_text(path)


    if path.exists():
        loaded = _load_sample()

    if not path.exists():
        _save_sample()

    elif (update is True
            and content is not None
            and content != loaded):
        _save_sample()


    return _load_sample()



def read_sample(
    sample: str,
    *,
    replace: Optional[DictStrAny] = None,
    prefix: bool = True,
) -> str:
    """
    Return the content after processing as the sample value.

    :param sample: Content that will be processed as sample.
    :param replace: Optional values to replace in the file.
    :param prefix: Determine whether or not prefix is added.
    :returns: Content after processing as the sample value.
    """

    replace = replace or {}

    items = replace.items()

    for new, old in items:

        if prefix is True:
            old = f'_/{PREFIX}/{old}/_'

        sample = rplstr(
            sample, new, old)

    return str(sample)



def rvrt_sample(
    sample: str,
    *,
    replace: Optional[DictStrAny] = None,
) -> str:
    """
    Return the content after processing as the sample value.

    :param sample: Content that will be processed as sample.
    :param replace: Optional values to replace in the file.
    :returns: Content after processing as the sample value.
    """

    replace = replace or {}

    items = replace.items()

    for new, old in items:

        new = f'_/{PREFIX}/{new}/_'

        sample = rplstr(
            sample, new, old)

    return str(sample)
