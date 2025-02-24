"""
Functions and routines associated with Enasis Network Common Library.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from copy import deepcopy
from pathlib import Path
from typing import Optional
from typing import TYPE_CHECKING

from .utils import config_load
from .utils import config_path
from .utils import config_paths
from ..types import DictStrAny
from ..types import merge_dicts
from ..types import sort_dict

if TYPE_CHECKING:
    from ..utils.common import PATHABLE



class ConfigFile:
    """
    Contain the configuration content from filesystem path.

    :param path: Complete or relative path to configuration.
    """

    path: Path
    config: DictStrAny


    def __init__(
        self,
        path: str | Path,
    ) -> None:
        """
        Initialize instance for class using provided parameters.
        """

        self.path = config_path(path)
        self.config = config_load(path)



class ConfigFiles:
    """
    Enumerate files and store the contents on relative path.

    .. note::
       Class can be empty in order to play nice with parent.

    :param paths: Complete or relative path to config files.
    :param force: Force the merge on earlier files by later.
    """

    paths: tuple[Path, ...]
    config: dict[str, ConfigFile]

    __merge: Optional[DictStrAny]


    def __init__(
        self,
        paths: 'PATHABLE',
        force: bool = False,
    ) -> None:
        """
        Initialize instance for class using provided parameters.
        """

        self.paths = config_paths(paths)

        self.config = {
            str(x): ConfigFile(x)
            for x in self.paths}

        self.__merge = None


    @property
    def merge(
        self,
    ) -> DictStrAny:
        """
        Return the configuration in dictionary format for files.

        :returns: Configuration in dictionary format for files.
        """

        config = self.config
        merge = self.__merge

        if merge is not None:
            return deepcopy(merge)

        merge = {}


        for file in config.values():

            source = file.config

            merge_dicts(
                dict1=merge,
                dict2=deepcopy(source),
                force=False)


        merge = sort_dict(merge)

        self.__merge = merge

        return deepcopy(merge)
