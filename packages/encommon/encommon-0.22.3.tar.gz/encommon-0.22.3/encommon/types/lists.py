"""
Functions and routines associated with Enasis Network Common Library.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from typing import Any
from typing import Sequence



def dedup_list(
    value: list[Any],
    update: bool = True,
) -> list[Any]:
    """
    Return the provided list values with duplicates removed.

    .. warning::
       This function will update the ``value`` reference.

    Example
    -------
    >>> value = [1, 2, 2, 3]
    >>> dedup_list(value)
    [1, 2, 3]
    >>> value
    [1, 2, 3]

    :param value: List of values processed for duplication.
    :param update: Indicate if to update provided reference.
    :returns: Provided list values with duplicates removed.
    """

    if update is False:
        value = list(value)


    unique: list[Any] = []

    for item in list(value):

        if item in unique:

            value.remove(item)

            continue

        unique.append(item)


    return value



def fuzzy_list(
    values: str | list[str],
    patterns: str | list[str],
) -> list[str]:
    """
    Return the provided values that match provided patterns.

    Example
    -------
    >>> values = ['foo', 'bar', 'baz', 'bop']
    >>> patterns = ['*o', 'ba*']
    >>> fuzzy_list(values, patterns)
    ['foo', 'bar', 'baz']

    :param values: Value or values to enumerate for matching.
    :param patterns: Patterns which values can match any one.
    :returns: Provided values that match provided patterns.
    """

    from ..utils import fuzz_match

    if isinstance(values, str):
        values = [values]

    matched: list[str] = []

    for value in values:

        match = fuzz_match(
            value, patterns)

        if match is False:
            continue

        matched.append(value)

    return matched



def inlist(
    needle: Any,  # noqa: ANN401
    haystack: Sequence[Any],
) -> bool:
    """
    Return the boolean indicating whether needle in haystack.

    Example
    -------
    >>> haystack = [1, 2, 3]
    >>> inlist(2, haystack)
    True

    :param needle: Provided item that may be within haystack.
    :param haystack: List of items which may contain needle.
    :returns: Boolean indicating whether needle in haystack.
    """

    return needle in haystack
