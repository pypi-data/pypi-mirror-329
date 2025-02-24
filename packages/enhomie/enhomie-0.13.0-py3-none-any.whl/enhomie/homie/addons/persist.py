"""
Functions and routines associated with Enasis Network Homie Automate.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from json import dumps
from json import loads
from threading import Lock
from typing import Annotated
from typing import Any
from typing import Literal
from typing import Optional
from typing import TYPE_CHECKING

from encommon.times import Time
from encommon.times import unitime
from encommon.times.common import UNITIME
from encommon.types import BaseModel
from encommon.types import DictStrAny
from encommon.types import merge_dicts

from pydantic import Field

from sqlalchemy import Column
from sqlalchemy import Float
from sqlalchemy import String
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Session
from sqlalchemy.orm import sessionmaker

if TYPE_CHECKING:
    from ..homie import Homie



HomiePersistValue = Optional[
    int | float | bool | str]

_PERSIST_VALUE = (
    int, float, bool, str)

HomiePersistLevel = Literal[
    'failure',
    'information',
    'success',
    'warning']

_PERSIST_ABOUT = {
    'unique': 'Unique key for the value',
    'value': 'Value stored at unique',
    'value_unit': 'Unit for persist value',
    'value_label': 'Label for persist value',
    'value_icon': 'Icon for persist value',
    'about': 'About the persist entry',
    'about_label': 'Label for persist entry',
    'about_icon': 'Icon for persist entry',
    'level': 'Severity of persist entry',
    'tags': 'Tags for persist entry',
    'expire': 'After when the key expires'}



class SQLBase(DeclarativeBase):
    """
    Some additional class that SQLAlchemy requires to work.
    """



class HomiePersistTable(SQLBase):
    """
    Schematic for the database operations using SQLAlchemy.

    .. note::
       Fields are not completely documented for this model.
    """

    unique = Column(
        String,
        primary_key=True,
        nullable=False)

    value = Column(
        String,
        nullable=False)

    value_unit = Column(
        String,
        nullable=True)

    value_label = Column(
        String,
        nullable=True)

    value_icon = Column(
        String,
        nullable=True)

    about = Column(
        String,
        nullable=True)

    about_label = Column(
        String,
        nullable=True)

    about_icon = Column(
        String,
        nullable=True)

    level = Column(
        String,
        nullable=True)

    tags = Column(
        String,
        nullable=True)

    expire = Column(
        Float,
        nullable=True)

    update = Column(
        Float,
        nullable=False)

    __tablename__ = 'persist'



_FIELD_UNIQUE = Annotated[
    str,
    Field(...,
          description=_PERSIST_ABOUT['unique'],
          min_length=1)]

_FIELD_VALUE = Annotated[
    HomiePersistValue,
    Field(...,
          description=_PERSIST_ABOUT['value'])]

_FIELD_VALUE_UNIT = Annotated[
    Optional[str],
    Field(None,
          description=_PERSIST_ABOUT['value_unit'],
          min_length=1)]

_FIELD_VALUE_LABEL = Annotated[
    Optional[str],
    Field(None,
          description=_PERSIST_ABOUT['value_label'],
          min_length=1)]

_FIELD_VALUE_ICON = Annotated[
    Optional[str],
    Field(None,
          description=_PERSIST_ABOUT['value_icon'],
          min_length=1)]

_FIELD_ABOUT = Annotated[
    Optional[str],
    Field(None,
          description=_PERSIST_ABOUT['about'],
          min_length=1)]

_FIELD_ABOUT_LABEL = Annotated[
    Optional[str],
    Field(None,
          description=_PERSIST_ABOUT['about_label'],
          min_length=1)]

_FIELD_ABOUT_ICON = Annotated[
    Optional[str],
    Field(None,
          description=_PERSIST_ABOUT['about_icon'],
          min_length=1)]

_FIELD_LEVEL = Annotated[
    Optional[HomiePersistLevel],
    Field(None,
          description=_PERSIST_ABOUT['level'],
          min_length=1)]

_FIELD_TAGS = Annotated[
    Optional[list[str]],
    Field(None,
          description=_PERSIST_ABOUT['tags'],
          min_length=1)]

_FIELD_EXPIRE = Annotated[
    Optional[str],
    Field(None,
          description='After when the key expires',
          min_length=20,
          max_length=32)]

_FIELD_UPDATE = Annotated[
    str,
    Field(...,
          description='When the value was updated',
          min_length=20,
          max_length=32)]



class HomiePersistRecord(BaseModel, extra='forbid'):
    """
    Contain the information regarding the persistent value.

    :param record: Record from the SQLAlchemy query routine.
    :param kwargs: Keyword arguments passed for downstream.
    """

    unique: _FIELD_UNIQUE

    value: _FIELD_VALUE

    value_unit: _FIELD_VALUE_UNIT

    value_label: _FIELD_VALUE_LABEL

    value_icon: _FIELD_VALUE_ICON

    about: _FIELD_ABOUT

    about_label: _FIELD_ABOUT_LABEL

    about_icon: _FIELD_ABOUT_ICON

    level: _FIELD_LEVEL

    tags: _FIELD_TAGS

    expire: _FIELD_EXPIRE

    update: _FIELD_UPDATE


    def __init__(
        self,
        record: Optional[HomiePersistTable] = None,
        **kwargs: Any,
    ) -> None:
        """
        Initialize instance for class using provided parameters.
        """

        params: DictStrAny

        fields = [
            'unique',
            'value',
            'value_unit',
            'value_label',
            'value_icon',
            'about',
            'about_label',
            'about_icon',
            'level',
            'tags',
            'expire',
            'update']


        if record is not None:

            params = {
                x: getattr(record, x)
                for x in fields}

            value = record.value
            tags = record.tags

            if value is not None:
                assert isinstance(value, str)
                params['value'] = loads(value)

            if tags is not None:
                assert isinstance(tags, str)
                params['tags'] = loads(tags)


        elif kwargs is not None:

            params = {
                x: kwargs.get(x)
                for x in fields}

        else:  # NOCVR
            raise ValueError('record')


        expire = params['expire']
        update = params['update']

        params['expire'] = (
            str(Time(expire))
            if expire is not None
            else None)

        params['update'] = (
            str(Time(update)))


        super().__init__(**params)



class HomiePersist:
    """
    Store the persistent information in the key value store.

    :param homie: Primary class instance for Homie Automate.
    """

    __homie: 'Homie'

    __connect: str
    __locker: Lock

    __sengine: Engine
    __session: (
        # pylint: disable=unsubscriptable-object
        sessionmaker[Session])


    def __init__(
        self,
        homie: 'Homie',
    ) -> None:
        """
        Initialize instance for class using provided parameters.
        """

        self.__homie = homie

        params = homie.params

        self.__connect = (
            params.database)

        self.__locker = Lock()

        self.__build_engine()


    def __build_engine(
        self,
    ) -> None:
        """
        Construct instances using the configuration parameters.
        """

        path = self.__connect

        sengine = (
            create_engine(path))

        (SQLBase.metadata
         .create_all(sengine))

        session = (
            sessionmaker(sengine))

        self.__sengine = sengine
        self.__session = session


    def insert(  # noqa: CFQ001,CFQ002
        self,
        unique: str,
        value: HomiePersistValue,
        expire: Optional[UNITIME] = None,
        *,
        value_unit: Optional[str] = None,
        value_label: Optional[str] = None,
        value_icon: Optional[str] = None,
        about: Optional[str] = None,
        about_label: Optional[str] = None,
        about_icon: Optional[str] = None,
        level: Optional[HomiePersistLevel] = None,
        tags: Optional[list[str]] = None,
        statics: Optional[DictStrAny] = None,
    ) -> None:
        """
        Insert the value within the persistent key value store.

        .. note::
           This will replace existing record with primary key.

        :param unique: Parameter value passed to the downstream.
        :param value: Parameter value passed to the downstream.
        :param value_unit: Parameter value passed to downstream.
        :param value_label: Parameter value passed to downstream.
        :param value_icon: Parameter value passed to downstream.
        :param expire: Parameter value passed to the downstream.
        :param about: Parameter value passed to the downstream.
        :param about_label: Parameter value passed to downstream.
        :param about_icon: Parameter value passed to downstream.
        :param level: Parameter value passed to the downstream.
        :param tags: Parameter value passed to the downstream.
        :param statics: Additional values available for parsing.
        """

        homie = self.__homie

        params = homie.params

        persists = (
            params.persists
            or {})

        statics = dict(statics or {})


        sess = self.__session()
        lock = self.__locker

        table = HomiePersistTable
        model = HomiePersistRecord


        if value is None:

            self.delete(unique)

            return None

        assert isinstance(
            value, _PERSIST_VALUE)


        # handle the timestamps

        update = Time().spoch

        if expire is not None:

            expire = unitime(expire)

            assert isinstance(
                expire, int)

            expire = update + expire


        # collect default values

        default: DictStrAny = {}

        if unique in persists:

            default = (
                persists[unique]
                .endumped)


        # collect input values

        inputs: DictStrAny = {
            'unique': unique,
            'value': value,
            'value_unit': value_unit,
            'value_label': value_label,
            'value_icon': value_icon,
            'about': about,
            'about_label': about_label,
            'about_icon': about_icon,
            'level': level,
            'tags': tags}

        inputs = {
            k: v for k, v
            in inputs.items()
            if v is not None}


        # merge the two together

        insert: DictStrAny = (
            merge_dicts(
                default, inputs,
                force=True,
                merge_list=False,
                merge_dict=False,
                paranoid=True))

        insert |= {
            'expire': expire,
            'update': update}

        statics |= {
            'record': insert}

        parsed = (
            homie.j2parse(
                value, statics))

        statics |= {
            'value': parsed}

        insert = (
            homie.j2parse(
                insert, statics))

        insert = (
            model(**insert)
            .endumped)


        # prepare the values

        value = insert['value']
        tags = insert['tags']
        expire = insert['expire']
        update = insert['update']

        insert['value'] = dumps(value)

        insert['tags'] = (
            dumps(tags)
            if tags is not None
            else None)

        insert['expire'] = (
            int(Time(expire))
            if expire is not None
            else None)

        insert['update'] = (
            int(Time(update)))


        # insert into database

        with lock, sess as session:

            session.merge(
                table(**insert))

            session.commit()


    def select(
        self,
        unique: str,
    ) -> HomiePersistValue:
        """
        Return the value from within persistent key value store.

        :param unique: Unique identifier from within the table.
        :returns: Value from within persistent key value store.
        """

        sess = self.__session()
        lock = self.__locker

        table = HomiePersistTable
        field = table.unique


        self.expire()


        with lock, sess as session:

            query = (
                session.query(table)
                .filter(field == unique))

            record = query.first()

            if record is None:
                return None

            value = str(record.value)

        value = loads(value)

        assert isinstance(
            value, _PERSIST_VALUE)

        return value


    def delete(
        self,
        unique: str,
    ) -> None:
        """
        Delete the value within the persistent key value store.

        :param unique: Unique identifier from within the table.
        """

        sess = self.__session()
        lock = self.__locker

        table = HomiePersistTable
        field = table.unique


        with lock, sess as session:

            query = (
                session.query(table)
                .filter(field == unique))

            record = query.first()

            if record is None:
                return None

            session.delete(record)

            session.commit()


    def expire(
        self,
    ) -> None:
        """
        Remove the expired persistent key values from the table.
        """

        sess = self.__session()
        lock = self.__locker

        table = HomiePersistTable
        expire = table.expire


        with lock, sess as session:

            now = Time().spoch

            (session.query(table)
             .filter(expire < now)
             .delete())

            session.commit()


    def record(
        self,
        unique: str,
    ) -> HomiePersistRecord:
        """
        Return the record within the persistent key value store.

        :param unique: Unique identifier from within the table.
        :returns: Record within the persistent key value store.
        """

        sess = self.__session()
        lock = self.__locker

        table = HomiePersistTable
        model = HomiePersistRecord
        field = table.unique

        self.expire()


        with lock, sess as session:

            query = (
                session.query(table)
                .filter(field == unique))

            record = query.first()

            assert record is not None

            return model(record)


    def records(
        self,
    ) -> list[HomiePersistRecord]:
        """
        Return all records within the persistent key value store.

        :returns: Records within the persistent key value store.
        """

        sess = self.__session()
        lock = self.__locker

        records: list[HomiePersistRecord]

        table = HomiePersistTable
        model = HomiePersistRecord


        with lock, sess as session:

            records = []

            query = (
                session.query(table))

            for record in query.all():

                object = model(record)

                records.append(object)

            return records
