"""
Functions and routines associated with Enasis Network Common Library.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from ..strings import hasstr
from ..strings import inrepr
from ..strings import instr
from ..strings import rplstr
from ..strings import strplwr



def test_strplwr() -> None:
    """
    Perform various tests associated with relevant routines.
    """

    assert strplwr(' Foo ') == 'foo'



def test_hasstr() -> None:
    """
    Perform various tests associated with relevant routines.
    """

    assert hasstr('abc', 'a')
    assert hasstr('abc', 'b')
    assert hasstr('abc', 'c')



def test_inrepr() -> None:
    """
    Perform various tests associated with relevant routines.
    """

    class MyClass:
        pass

    item = MyClass()

    assert inrepr('MyClass', item)



def test_instr() -> None:
    """
    Perform various tests associated with relevant routines.
    """

    class MyClass:
        pass

    item = MyClass()

    assert instr('MyClass', item)



def test_rplstr() -> None:
    """
    Perform various tests associated with relevant routines.
    """

    string = rplstr('foo', 'o', 'O')

    assert string == 'fOO'
