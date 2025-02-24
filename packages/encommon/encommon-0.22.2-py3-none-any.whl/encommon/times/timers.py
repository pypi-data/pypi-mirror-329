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
from .params import TimersParams
from .time import Time
from .timer import Timer

if TYPE_CHECKING:
    from .params import TimerParams



TIMERS = dict[str, Timer]



class SQLBase(DeclarativeBase):
    """
    Some additional class that SQLAlchemy requires to work.

    .. note::
       Input parameters are not defined, check parent class.
    """



class TimersTable(SQLBase):
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

    update = Column(
        String,
        nullable=False)

    __tablename__ = 'timers'



class Timers:
    """
    Track timers on unique key determining when to proceed.

    .. warning::
       This class will use an in-memory database for cache,
       unless a cache file is explicity defined.

    .. testsetup::
       >>> from .params import TimerParams
       >>> from .params import TimersParams
       >>> from time import sleep

    Example
    -------
    >>> source = {'one': TimerParams(timer=1)}
    >>> params = TimersParams(timers=source)
    >>> timers = Timers(params)
    >>> timers.ready('one')
    False
    >>> sleep(1)
    >>> timers.ready('one')
    True

    :param params: Parameters used to instantiate the class.
    :param store: Optional database path for keeping state.
    :param group: Optional override for default group name.
    """

    __params: 'TimersParams'

    __store: str
    __group: str

    __store_engine: Engine
    __store_session: (
        # pylint: disable=unsubscriptable-object
        sessionmaker[Session])

    __timers: TIMERS


    def __init__(
        self,
        params: Optional['TimersParams'] = None,
        *,
        store: str = 'sqlite:///:memory:',
        group: str = 'default',
    ) -> None:
        """
        Initialize instance for class using provided parameters.
        """

        params = deepcopy(params)

        if params is None:
            params = TimersParams()

        self.__params = params


        self.__store = store
        self.__group = group

        self.__make_engine()


        self.__timers = {}

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
    ) -> 'TimersParams':
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
    def children(
        self,
    ) -> dict[str, Timer]:
        """
        Return the value for the attribute from class instance.

        :returns: Value for the attribute from class instance.
        """

        return dict(self.__timers)


    def load_children(
        self,
    ) -> None:
        """
        Construct the children instances for the primary class.
        """

        params = self.__params
        timers = self.__timers

        group = self.__group

        session = self.store_session

        config = params.timers


        _table = TimersTable
        _group = _table.group
        _unique = _table.unique

        query = (
            session.query(_table)
            .filter(_group == group)
            .order_by(_unique))

        for record in query.all():

            unique = str(record.unique)
            last = str(record.last)

            if unique not in config:
                continue

            _config = config[unique]

            _config.start = last


        items = config.items()

        for key, value in items:

            if key in timers:

                timer = timers[key]

                timer.update(value.start)

                continue

            timer = Timer(
                value.timer,
                start=value.start)

            timers[key] = timer


        self.__timers = timers


    def save_children(
        self,
    ) -> None:
        """
        Save the child caches from the attribute into database.
        """

        timers = self.__timers

        group = self.__group

        session = self.store_session


        items = timers.items()

        for unique, timer in items:

            update = Time('now')

            append = TimersTable(
                group=group,
                unique=unique,
                last=timer.time.subsec,
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

        timers = self.__timers

        if unique not in timers:
            raise ValueError('unique')

        timer = timers[unique]

        ready = timer.ready(update)

        if ready is True:
            self.save_children()

        return ready


    def pause(
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

        return not self.ready(
            unique, update)


    def create(
        self,
        unique: str,
        params: 'TimerParams',
    ) -> Timer:
        """
        Create a new timer using the provided input parameters.

        :param unique: Unique identifier for the related child.
        :param params: Parameters used to instantiate the class.
        :returns: Newly constructed instance of related class.
        """

        config = (
            self.params
            .timers)

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
        Update the timer from the provided parasable time value.

        :param unique: Unique identifier for the related child.
        :param value: Override the time updated for timer value.
        """

        timers = self.__timers

        if unique not in timers:
            raise ValueError('unique')

        timer = timers[unique]

        timer.update(value)

        self.save_children()


    def delete(
        self,
        unique: str,
    ) -> None:
        """
        Delete the timer from the internal dictionary reference.

        .. note::
           This is a graceful method, will not raise exception
           when the provided unique value does not exist.

        :param unique: Unique identifier for the related child.
        """

        params = self.__params
        timers = self.__timers

        group = self.__group

        session = self.store_session

        config = params.timers


        if unique in config:
            del config[unique]

        if unique in timers:
            del timers[unique]


        _table = TimersTable
        _group = _table.group
        _unique = _table.unique

        (session.query(_table)
         .filter(_unique == unique)
         .filter(_group == group)
         .delete())


        session.commit()
        session.close()
