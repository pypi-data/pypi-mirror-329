"""
Functions and routines associated with Enasis Network Common Library.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from ..unitime import unitime



def test_unitime() -> None:
    """
    Perform various tests associated with relevant routines.
    """

    assert unitime('1s') == 1
    assert unitime('1h') == 3600
    assert unitime('1') == 1
    assert unitime(1) == 1
    assert unitime('1.0') == 1
