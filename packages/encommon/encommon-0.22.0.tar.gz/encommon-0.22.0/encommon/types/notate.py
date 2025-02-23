"""
Functions and routines associated with Enasis Network Common Library.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from contextlib import suppress
from re import compile
from re import match as re_match
from typing import Any
from typing import Optional
from typing import Union

from .empty import Empty
from .types import DictStrAny



_INTEGER = compile(r'^\d+$')
_INDICES = (list, tuple, dict)
_RECURSE = dict



_SETABLE = Union[
    DictStrAny,
    list[Any]]

_GETABLE = Union[
    tuple[Any, ...],
    _SETABLE]



def getate(
    source: _GETABLE,
    path: str,
    default: Optional[Any] = None,
    delim: str = '/',
) -> Any:  # noqa: ANN401
    """
    Collect the value within the dictionary using notation.

    Example
    -------
    >>> source = {'foo': {'bar': 'baz'}}
    >>> getate(source, 'foo/bar')
    'baz'

    Example
    -------
    >>> source = {'foo': ['bar', 'baz']}
    >>> getate(source, 'foo/1')
    'baz'

    :param source: Dictionary object processed in notation.
    :param path: Path to the value within the source object.
    :param default: Value to use if none is found in source.
    :param delim: Override default delimiter between parts.
    :returns: Value that was located within provided source.
    """

    sourze: Any = source

    split = path.split(delim)

    length = len(split)


    items = enumerate(split)

    for index, base in items:

        if sourze is Empty:
            return default


        indices = isinstance(
            sourze, _INDICES)

        if (indices is False
                and index < length):
            return default


        recurse = isinstance(
            sourze, _RECURSE)

        if recurse is False:

            with suppress(IndexError):
                sourze = sourze[int(base)]
                continue


        if base not in sourze:
            sourze = Empty
            continue

        sourze = sourze[base]


    return (
        default if sourze is Empty
        else sourze)



def setate(
    source: _SETABLE,
    path: str,
    value: Any,  # noqa: ANN401
    delim: str = '/',
) -> None:
    """
    Define the value within the dictionary using notation.

    Example
    -------
    >>> source = {'foo': {'bar': 'baz'}}
    >>> source['foo']['bar']
    'baz'
    >>> setate(source, 'foo/bar', 'bop')
    >>> source['foo']['bar']
    'bop'

    :param source: Dictionary object processed in notation.
    :param path: Path to the value within the source object.
    :param value: Value which will be defined at noted point.
    :param delim: Override default delimiter between parts.
    """

    _setvalue(source, path, value, delim)



def delate(
    source: _SETABLE,
    path: str,
    delim: str = '/',
) -> None:
    """
    Delete the value within the dictionary using notation.

    Example
    -------
    >>> source = {'foo': {'bar': 'baz'}}
    >>> delate(source, 'foo/bar')
    >>> source
    {'foo': {}}

    :param source: Dictionary object processed in notation.
    :param path: Path to the value within the source object.
    :param delim: Override default delimiter between parts.
    """

    split = path.split(delim)

    with suppress(KeyError, IndexError):


        for part in split[:-1]:

            setable = isinstance(
                source, dict | list)

            if setable is False:
                raise ValueError('source')

            if isinstance(source, list):
                source = source[int(part)]

            elif isinstance(source, dict):
                source = source[part]


        part = split[-1]

        setable = isinstance(
            source, dict | list)

        if setable is False:
            raise ValueError('source')

        if isinstance(source, dict):
            del source[part]

        if isinstance(source, list):
            del source[int(part)]



def impate(  # noqa: CFQ001,CFQ004
    source: DictStrAny | list[DictStrAny],
    delim: str = '/',
    parent: Optional[str] = None,
    *,
    implode_list: bool = True,
    recurse_list: bool = True,
) -> DictStrAny | list[DictStrAny]:
    """
    Implode the dictionary into a single depth of notation.

    Example
    -------
    >>> impate({'foo': {'bar': 'baz'}})
    {'foo/bar': 'baz'}

    :param source: Dictionary object processed in notation.
    :param delim: Override default delimiter between parts.
    :param parent: Parent key prefix for downstream update.
    :param implode_list: Determine whether list is imploded.
    :param recurse_list: Determine whether flatten in list.
    :returns: New dictionary that was recursively imploded.
        It is also possible that a list of dictionary will
        be returned when provided and implode_list is False.
    """

    _implode = implode_list
    _recurse = recurse_list


    def _proclist(
        source: list[Any],
        delim: str,
        parent: Optional[str],
    ) -> DictStrAny | list[Any]:


        if _implode is False:

            process = [
                (impate(
                    item, delim,
                    implode_list=_implode,
                    recurse_list=_recurse)
                 if isinstance(item, dict | list)
                 and _recurse is True
                 else item)
                for item in source]

            return (
                {parent: process}
                if parent is not None
                else process)


        returned: DictStrAny = {}

        for i, item in enumerate(source):

            key = (
                f'{parent}{delim}{i}'
                if parent is not None
                else str(i))

            if (isinstance(item, dict | list)
                    and _recurse is True):

                implode = impate(
                    item, delim, key,
                    implode_list=_implode,
                    recurse_list=_recurse)

                assert isinstance(implode, dict)

                returned.update(implode)

            else:
                returned[key] = item

        return returned


    def _procdict(
        source: DictStrAny,
        delim: str,
        parent: Optional[str],
    ) -> DictStrAny:

        returned: DictStrAny = {}

        for key, value in source.items():

            key = (
                f'{parent}{delim}{key}'
                if parent is not None
                else key)

            if isinstance(value, dict):

                implode = impate(
                    value, delim, key,
                    implode_list=_implode,
                    recurse_list=_recurse)

                assert isinstance(implode, dict)

                returned |= implode

            elif isinstance(value, list):

                process = _proclist(
                    value, delim, key)

                returned |= (
                    {key: process}
                    if not isinstance(process, dict)
                    else process)

            else:
                returned[key] = value

        return returned


    if isinstance(source, dict):
        return _procdict(
            source, delim, parent)

    if isinstance(source, list):
        return _proclist(
            source, delim, parent)

    raise ValueError('source')



def expate(
    source: DictStrAny,
    delim: str = '/',
) -> DictStrAny:
    """
    Explode the dictionary from a single depth of notation.

    Example
    -------
    >>> expate({'foo/bar': 'baz'})
    {'foo': {'bar': 'baz'}}

    :param source: Dictionary object processed in notation.
    :param delim: Override default delimiter between parts.
    :returns: New dictionary that was recursively exploded.
    """

    returned: DictStrAny = {}


    items = source.items()

    for key, value in items:

        if isinstance(value, list):
            value = [
                (expate(x, delim)
                 if isinstance(x, dict)
                 else x)
                for x in value]

        if isinstance(value, dict):
            value = expate(value, delim)

        setate(
            returned, key,
            value, delim)


    return returned



def _setpath(
    source: _SETABLE,
    path: str,
    value: Any,  # noqa: ANN401
    delim: str = '/',
) -> None:
    """
    Define the value within the dictionary using notation.

    .. note::
       This is a private helper function that could change.

    :param source: Dictionary object processed in notation.
    :param path: Path to the value within the source object.
    :param value: Value which will be defined at noted point.
    :param delim: Override default delimiter between parts.
    """


    setable = isinstance(
        source, dict | list)

    assert setable is True


    base, path = (
        path.split(delim, 1))

    next = (
        path.split(delim, 1)[0])


    default: _SETABLE = {}

    if re_match(_INTEGER, next):
        default = []

    update: Any


    if isinstance(source, list):

        length = len(source)
        index = int(base)

        update = default

        with suppress(IndexError):
            update = source[index]

        _setvalue(
            update, path,
            value, delim)

        if length == index:
            source.append(update)

        elif length > index:
            source[index] = update


    elif isinstance(source, dict):

        update = default

        with suppress(KeyError):
            update = source[base]

        _setvalue(
            update, path,
            value, delim)

        source[base] = update



def _setvalue(
    source: _SETABLE,
    path: str,
    value: Any,  # noqa: ANN401
    delim: str = '/',
) -> None:
    """
    Define the value within the dictionary using notation.

    .. note::
       This is a private helper function that could change.

    :param source: Dictionary object processed in notation.
    :param path: Path to the value within the source object.
    :param value: Value which will be defined at noted point.
    :param delim: Override default delimiter between parts.
    """


    setable = isinstance(
        source, dict | list)

    if setable is False:
        raise ValueError('source')


    if delim in path:
        return _setpath(
            source, path,
            value, delim)


    if isinstance(source, list):

        length = len(source)
        index = int(path)

        if index > length:
            raise IndexError(index)

        if length == index:
            source.append(value)

        elif length > index:
            source[index] = value


    if isinstance(source, dict):
        source[path] = value
