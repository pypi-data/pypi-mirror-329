"""
Functions and routines associated with Enasis Network Common Library.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from copy import deepcopy
from typing import Callable
from typing import Optional
from typing import TYPE_CHECKING

from .files import ConfigFiles
from .logger import Logger
from .params import Params
from .paths import ConfigPaths
from .utils import config_paths
from ..crypts import Crypts
from ..types import DictStrAny
from ..types import merge_dicts
from ..types import setate
from ..types import sort_dict

if TYPE_CHECKING:
    from ..utils.common import PATHABLE



class Config:
    """
    Contain the configurations from the arguments and files.

    .. note::
       Configuration loaded from files is validated with the
       Pydantic model :class:`encommon.config.Params`.

    .. testsetup::
       >>> from pathlib import Path
       >>> path = str(getfixture('tmpdir'))

    Example
    -------
    >>> config = Config()
    >>> config.config
    {'enconfig': None, 'encrypts': None, 'enlogger': None}

    :param files: Complete or relative path to config files.
    :param paths: Complete or relative path to config paths.
    :param cargs: Configuration arguments in dictionary form,
        which will override contents from the config files.
    :param sargs: Additional arguments on the command line.
    :param model: Override default config validation model.
    """

    __files: ConfigFiles
    __paths: ConfigPaths
    __cargs: DictStrAny
    __sargs: DictStrAny

    __model: Callable  # type: ignore

    __params: Optional[Params]
    __logger: Optional[Logger]
    __crypts: Optional[Crypts]


    def __init__(
        self,
        files: Optional['PATHABLE'] = None,
        *,
        paths: Optional['PATHABLE'] = None,
        cargs: Optional[DictStrAny] = None,
        sargs: Optional[DictStrAny] = None,
        model: Optional[Callable] = None,  # type: ignore
    ) -> None:
        """
        Initialize instance for class using provided parameters.
        """

        files = files or []
        paths = paths or []
        cargs = cargs or {}
        sargs = sargs or {}

        paths = list(config_paths(paths))

        self.__model = model or Params
        self.__files = ConfigFiles(files)
        self.__cargs = deepcopy(cargs)
        self.__sargs = deepcopy(sargs)

        self.__params = None

        enconfig = (
            self.params.enconfig)

        if enconfig and enconfig.paths:
            paths.extend(enconfig.paths)

        self.__paths = ConfigPaths(paths)

        self.__logger = None
        self.__crypts = None


    @property
    def files(
        self,
    ) -> ConfigFiles:
        """
        Return the value for the attribute from class instance.

        :returns: Value for the attribute from class instance.
        """

        return self.__files


    @property
    def paths(
        self,
    ) -> ConfigPaths:
        """
        Return the value for the attribute from class instance.

        :returns: Value for the attribute from class instance.
        """

        return self.__paths


    @property
    def cargs(
        self,
    ) -> DictStrAny:
        """
        Return the value for the attribute from class instance.

        :returns: Value for the attribute from class instance.
        """

        returned: DictStrAny = {}

        cargs = deepcopy(self.__cargs)

        items = cargs.items()

        for key, value in items:
            setate(returned, key, value)

        return deepcopy(returned)


    @property
    def sargs(
        self,
    ) -> DictStrAny:
        """
        Return the value for the attribute from class instance.

        :returns: Value for the attribute from class instance.
        """

        returned: DictStrAny = {}

        sargs = deepcopy(self.__sargs)

        items = sargs.items()

        for key, value in items:
            setate(returned, key, value)

        return deepcopy(returned)


    @property
    def basic(
        self,
    ) -> DictStrAny:
        """
        Return the configuration source loaded from the objects.

        :returns: Configuration source loaded from the objects.
        """

        files = self.__files

        ferged = files.merge

        merge_dicts(
            dict1=ferged,
            dict2=self.cargs,
            force=True)

        return deepcopy(ferged)


    @property
    def merge(
        self,
    ) -> DictStrAny:
        """
        Return the configuration source loaded from the objects.

        :returns: Configuration source loaded from the objects.
        """

        files = self.__files
        paths = self.__paths

        ferged = files.merge
        perged = paths.merge

        merge_dicts(
            dict1=ferged,
            dict2=self.cargs,
            force=True)

        values = perged.values()

        for merge in values:

            merge_dicts(
                dict1=ferged,
                dict2=merge,
                force=False)

        return deepcopy(ferged)


    @property
    def model(
        self,
    ) -> Callable:  # type: ignore
        """
        Return the value for the attribute from class instance.

        :returns: Value for the attribute from class instance.
        """

        return self.__model


    @property
    def params(
        self,
    ) -> Params:
        """
        Return the Pydantic model containing the configuration.

        :returns: Pydantic model containing the configuration.
        """

        params = self.__params

        if params is not None:
            return params

        params = self.model(
            **self.basic)

        self.__params = params

        return self.__params


    @property
    def config(
        self,
    ) -> DictStrAny:
        """
        Return the configuration dumped from the Pydantic model.

        :returns: Configuration dumped from the Pydantic model.
        """

        return sort_dict(self.params.endumped)


    @property
    def logger(
        self,
    ) -> Logger:
        """
        Initialize the Python logging library using parameters.

        :returns: Instance of Python logging library created.
        """

        logger = self.__logger
        params = self.params

        if logger is not None:
            return logger

        logger = Logger(
            params.enlogger)

        self.__logger = logger

        return self.__logger


    @property
    def crypts(
        self,
    ) -> Crypts:
        """
        Initialize the encryption instance using the parameters.

        :returns: Instance of the encryption instance created.
        """

        crypts = self.__crypts
        params = self.params

        if crypts is not None:
            return crypts

        crypts = Crypts(
            params.encrypts)

        self.__crypts = crypts

        return self.__crypts
