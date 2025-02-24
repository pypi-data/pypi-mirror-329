"""
Functions and routines associated with Enasis Network Homie Automate.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from typing import TYPE_CHECKING

from encommon.types import inrepr
from encommon.types import instr
from encommon.types import lattrs

if TYPE_CHECKING:
    from ...homie import Homie



def test_HomiePersist(
    homie: 'Homie',
) -> None:
    """
    Perform various tests associated with relevant routines.

    :param homie: Primary class instance for Homie Automate.
    """

    persist = homie.persist


    attrs = lattrs(persist)

    assert attrs == [
        '_HomiePersist__homie',
        '_HomiePersist__connect',
        '_HomiePersist__locker',
        '_HomiePersist__sengine',
        '_HomiePersist__session']


    assert inrepr(
        'persist.HomiePersist',
        persist)

    assert isinstance(
        hash(persist), int)

    assert instr(
        'persist.HomiePersist',
        persist)


    persist.insert(
        'jupiter_aspire',
        False)

    value = (
        persist
        .select('jupiter_aspire'))

    assert value is False


    record = (
        persist
        .record('jupiter_aspire')
        .endumped)

    assert record == {
        'about': 'Aspire for Jupiter',
        'about_icon': 'jupiter',
        'about_label': 'Jupiter Aspire',
        'expire': None,
        'level': 'information',
        'tags': ['jupiter', 'aspire'],
        'unique': 'jupiter_aspire',
        'update': record['update'],
        'value': False,
        'value_icon': None,
        'value_label': 'Current Status',
        'value_unit': 'status'}


    persist.delete(
        'jupiter_aspire')

    value = (
        persist
        .select('jupiter_aspire'))

    assert value is None


    persist.insert(
        'jupiter_aspire',
        value=True,
        expire=-1)

    value = (
        persist
        .select('jupiter_aspire'))

    assert value is None



def test_HomiePersist_cover(  # noqa: CFQ001
    homie: 'Homie',
) -> None:
    """
    Perform various tests associated with relevant routines.

    :param homie: Primary class instance for Homie Automate.
    """

    persist = homie.persist


    persist.insert(
        unique='present',
        value=None)

    value = (
        persist
        .select('present'))

    assert value is None

    records = persist.records()

    assert len(records) == 0


    persist.insert(
        unique='types',
        value=1,
        tags=['one', 'two'])

    value = (
        persist
        .select('types'))

    assert value == 1

    records = persist.records()

    assert len(records) == 1

    record = records[0].endumped

    assert record == {
        'about': None,
        'about_icon': None,
        'about_label': None,
        'expire': record['expire'],
        'level': None,
        'tags': ['one', 'two'],
        'unique': 'types',
        'update': record['update'],
        'value': 1,
        'value_icon': None,
        'value_label': None,
        'value_unit': None}


    persist.insert(
        unique='types',
        value=1.0)

    value = (
        persist
        .select('types'))

    assert value == 1.0

    records = persist.records()

    assert len(records) == 1
    assert records[0].unique == 'types'
    assert records[0].value == 1.0


    persist.insert(
        unique='types',
        value='string')

    value = (
        persist
        .select('types'))

    assert value == 'string'

    records = persist.records()

    assert len(records) == 1
    assert records[0].unique == 'types'
    assert records[0].value == 'string'


    persist.insert(
        unique='types',
        value=True)

    value = (
        persist
        .select('types'))

    assert value is True

    records = persist.records()

    assert len(records) == 1
    assert records[0].unique == 'types'
    assert records[0].value is True


    persist.insert(
        unique='types',
        value=None)

    value = (
        persist
        .select('types'))

    assert value is None

    records = persist.records()

    assert len(records) == 0
