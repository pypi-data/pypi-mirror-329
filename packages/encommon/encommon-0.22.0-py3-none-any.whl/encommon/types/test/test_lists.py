"""
Functions and routines associated with Enasis Network Common Library.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from ..lists import dedup_list
from ..lists import fuzzy_list
from ..lists import inlist



def test_inlist() -> None:
    """
    Perform various tests associated with relevant routines.
    """

    needle = 123

    haystack = [123, 456]

    assert inlist(needle, haystack)



def test_dedup_list() -> None:
    """
    Perform various tests associated with relevant routines.
    """

    value = [1, 1, '2', 2, 3, 3]

    dedup = dedup_list(
        value,
        update=False)

    assert dedup != value
    assert dedup == [1, '2', 2, 3]

    dedup_list(value)

    assert dedup == value
    assert dedup == [1, '2', 2, 3]



def test_fuzzy_list() -> None:
    """
    Perform various tests associated with relevant routines.
    """

    values = ['1', '2']
    patterns = ['1*']

    matched = fuzzy_list(
        values, patterns)

    assert matched == ['1']

    assert not (
        fuzzy_list('', []))
