"""
Functions and routines associated with Enasis Network Common Library.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from copy import deepcopy
from typing import Optional
from typing import TYPE_CHECKING

from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Session
from sqlalchemy.orm import sessionmaker

from .common import PARSABLE
from .params import WindowsParams
from .time import Time
from .window import Window

if TYPE_CHECKING:
    from .params import WindowParams



WINDOWS = dict[str, Window]



class SQLBase(DeclarativeBase):
    """
    Some additional class that SQLAlchemy requires to work.

    .. note::
       Input parameters are not defined, check parent class.
    """



class WindowsTable(SQLBase):
    """
    Schematic for the database operations using SQLAlchemy.

    .. note::
       Fields are not completely documented for this model.
    """

    group = Column(
        String,
        primary_key=True,
        nullable=False)

    unique = Column(
        String,
        primary_key=True,
        nullable=False)

    last = Column(
        String,
        nullable=False)

    next = Column(
        String,
        nullable=False)

    update = Column(
        String,
        nullable=False)

    __tablename__ = 'windows'



class Windows:
    """
    Track windows on unique key determining when to proceed.

    .. warning::
       This class will use an in-memory database for cache,
       unless a cache file is explicity defined.

    .. testsetup::
       >>> from .params import WindowParams
       >>> from .params import WindowsParams

    Example
    -------
    >>> source = {'one': WindowParams(window=1)}
    >>> params = WindowsParams(windows=source)
    >>> windows = Windows(params, '-2s', 'now')
    >>> [windows.ready('one') for x in range(3)]
    [True, True, False]

    :param params: Parameters used to instantiate the class.
    :param start: Determine the start for scheduling window.
    :param stop: Determine the ending for scheduling window.
    :param store: Optional database path for keeping state.
    :param group: Optional override for default group name.
    """

    __params: 'WindowsParams'

    __store: str
    __group: str

    __store_engine: Engine
    __store_session: (
        # pylint: disable=unsubscriptable-object
        sessionmaker[Session])

    __start: Time
    __stop: Time

    __windows: WINDOWS


    def __init__(
        self,
        params: Optional['WindowsParams'] = None,
        start: PARSABLE = 'now',
        stop: PARSABLE = '3000-01-01',
        *,
        store: str = 'sqlite:///:memory:',
        group: str = 'default',
    ) -> None:
        """
        Initialize instance for class using provided parameters.
        """

        params = deepcopy(params)

        if params is None:
            params = WindowsParams()

        self.__params = params


        self.__store = store
        self.__group = group

        self.__make_engine()


        start = Time(start)
        stop = Time(stop)

        assert stop > start

        self.__start = start
        self.__stop = stop


        self.__windows = {}

        self.load_children()


    def __make_engine(
        self,
    ) -> None:
        """
        Construct instances using the configuration parameters.
        """

        store = self.__store

        engine = create_engine(store)

        (SQLBase.metadata
         .create_all(engine))

        session = sessionmaker(engine)

        self.__store_engine = engine
        self.__store_session = session


    @property
    def params(
        self,
    ) -> 'WindowsParams':
        """
        Return the Pydantic model containing the configuration.

        :returns: Pydantic model containing the configuration.
        """

        return self.__params


    @property
    def store(
        self,
    ) -> str:
        """
        Return the value for the attribute from class instance.

        :returns: Value for the attribute from class instance.
        """

        return self.__store


    @property
    def group(
        self,
    ) -> str:
        """
        Return the value for the attribute from class instance.

        :returns: Value for the attribute from class instance.
        """

        return self.__group


    @property
    def store_engine(
        self,
    ) -> Engine:
        """
        Return the value for the attribute from class instance.

        :returns: Value for the attribute from class instance.
        """

        return self.__store_engine


    @property
    def store_session(
        self,
    ) -> Session:
        """
        Return the value for the attribute from class instance.

        :returns: Value for the attribute from class instance.
        """

        return self.__store_session()


    @property
    def start(
        self,
    ) -> Time:
        """
        Return the value for the attribute from class instance.

        :returns: Value for the attribute from class instance.
        """

        return Time(self.__start)


    @property
    def stop(
        self,
    ) -> Time:
        """
        Return the value for the attribute from class instance.

        :returns: Value for the attribute from class instance.
        """

        return Time(self.__stop)


    @property
    def children(
        self,
    ) -> dict[str, Window]:
        """
        Return the value for the attribute from class instance.

        :returns: Value for the attribute from class instance.
        """

        return dict(self.__windows)


    def load_children(
        self,
    ) -> None:
        """
        Construct the children instances for the primary class.
        """

        params = self.__params
        windows = self.__windows

        start = self.__start
        stop = self.__stop

        group = self.__group

        session = self.store_session

        config = params.windows


        _table = WindowsTable
        _group = _table.group
        _unique = _table.unique

        query = (
            session.query(_table)
            .filter(_group == group)
            .order_by(_unique))

        for record in query.all():

            unique = str(record.unique)
            next = str(record.next)

            if unique not in config:
                continue

            _config = config[unique]

            _config.start = next
            _config.anchor = next


        items = config.items()

        for key, value in items:

            if key in windows:

                window = windows[key]

                window.update(value.start)

                continue

            _start = (
                value.start or start)

            _stop = (
                value.stop or stop)

            if _start < start:
                _start = start

            if _stop > stop:
                _stop = stop

            _anchor = (
                value.anchor or _start)

            window = Window(
                value.window,
                start=_start,
                stop=_stop,
                anchor=_anchor,
                delay=value.delay)

            windows[key] = window


        self.__windows = windows


    def save_children(
        self,
    ) -> None:
        """
        Save the child caches from the attribute into database.
        """

        windows = self.__windows

        group = self.__group

        session = self.store_session


        items = windows.items()

        for unique, window in items:

            update = Time('now')

            append = WindowsTable(
                group=group,
                unique=unique,
                last=window.last.subsec,
                next=window.next.subsec,
                update=update.subsec)

            session.merge(append)


        session.commit()
        session.close()


    def ready(
        self,
        unique: str,
        update: bool = True,
    ) -> bool:
        """
        Determine whether or not the appropriate time has passed.

        :param unique: Unique identifier for the related child.
        :param update: Determines whether or not time is updated.
        :returns: Boolean indicating whether enough time passed.
        """

        windows = self.__windows

        if unique not in windows:
            raise ValueError('unique')

        window = windows[unique]

        ready = window.ready(update)

        if ready is True:
            self.save_children()

        return ready


    def create(
        self,
        unique: str,
        params: 'WindowParams',
    ) -> Window:
        """
        Create a new window using the provided input parameters.

        :param unique: Unique identifier for the related child.
        :param params: Parameters used to instantiate the class.
        :returns: Newly constructed instance of related class.
        """

        config = (
            self.params
            .windows)

        if unique in config:
            raise ValueError('unique')

        config[unique] = params

        self.load_children()

        self.save_children()

        return self.children[unique]


    def update(
        self,
        unique: str,
        value: Optional[PARSABLE] = None,
    ) -> None:
        """
        Update the window from the provided parasable time value.

        :param unique: Unique identifier for the related child.
        :param value: Override the time updated for window value.
        """

        windows = self.__windows

        if unique not in windows:
            raise ValueError('unique')

        window = windows[unique]

        window.update(value)

        self.save_children()


    def delete(
        self,
        unique: str,
    ) -> None:
        """
        Delete the window from the internal dictionary reference.

        .. note::
           This is a graceful method, will not raise exception
           when the provided unique value does not exist.

        :param unique: Unique identifier for the related child.
        """

        params = self.__params
        windows = self.__windows

        group = self.__group

        session = self.store_session

        config = params.windows


        if unique in config:
            del config[unique]

        if unique in windows:
            del windows[unique]


        _table = WindowsTable
        _group = _table.group
        _unique = _table.unique

        (session.query(_table)
         .filter(_unique == unique)
         .filter(_group == group)
         .delete())


        session.commit()
        session.close()
