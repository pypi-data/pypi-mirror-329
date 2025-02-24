"""
Functions and routines associated with Enasis Network Common Library.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from pydantic import BaseModel as Pydantic

from .types import DictStrAny



class BaseModel(Pydantic, extra='forbid'):
    """
    Pydantic base model but with added methods and routines.

    :param data: Keyword arguments passed to Pydantic model.
    """


    @property
    def endumped(
        self,
    ) -> DictStrAny:
        """
        Return the facts about the attributes from the instance.

        :returns: Facts about the attributes from the instance.
        """

        return self.model_dump()


    @property
    def enpruned(
        self,
    ) -> DictStrAny:
        """
        Return the facts about the attributes from the instance.

        :returns: Facts about the attributes from the instance.
        """

        return self.model_dump(
            exclude_none=True)



def clsname(
    cls: object,
) -> str:
    """
    Return the actual definition name for the Python class.

    :param cls: Provided Python class related to operation.
    :returns: Actual definition name for the Python class.
    """

    assert hasattr(
        cls, '__class__')

    _cls = cls.__class__

    assert hasattr(
        _cls, '__name__')

    return str(_cls.__name__)



def lattrs(
    cls: object,
) -> list[str]:
    """
    Return the list of attributes which are found in class.

    :param cls: Provided Python class related to operation.
    :returns: List of attributes which are found in class.
    """

    return list(cls.__dict__)
