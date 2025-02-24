"""
Functions and routines associated with Enasis Network Homie Automate.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from copy import deepcopy
from typing import Literal
from typing import Optional
from typing import TYPE_CHECKING

from encommon.types import DictStrAny
from encommon.types import NCFalse
from encommon.types import merge_dicts
from encommon.types import strplwr

if TYPE_CHECKING:
    from ..homie.common import HomieKinds



UbiqFetch = DictStrAny
UbiqMerge = dict[str, UbiqFetch]

UbiqKinds = Literal[
    'historic',
    'realtime']



def merge_fetch(
    fetch: UbiqFetch,
) -> UbiqMerge:
    """
    Return the content related to the item in parent system.

    :param fetch: Dictionary from the origin to be updated.
    :returns: Content related to the item in parent system.
    """

    fetch = deepcopy(fetch)


    staged: UbiqMerge = {}
    source: UbiqMerge = {}

    historic = (
        fetch['historic']
        ['data'])

    realtime = (
        fetch['realtime']
        ['data'])


    def _fixtimes(
        fetch: UbiqFetch,
    ) -> None:

        if 'first_seen' in item:
            item['first_seen'] = [
                item['first_seen']]

        if 'last_seen' in item:
            item['last_seen'] = [
                item['last_seen']]


    def _combine(
        target: UbiqKinds,
    ) -> None:

        unique = item['_id']

        if unique not in staged:
            staged[unique] = {}

        source = staged[unique]

        assert target not in source

        _fixtimes(item)

        source[target] = (
            deepcopy(item))


    for item in historic:
        _combine('historic')

    for item in realtime:
        _combine('realtime')


    items = staged.items()

    for unique, fetch in items:

        historic = deepcopy(
            fetch.get('historic')
            or {})

        realtime = deepcopy(
            fetch.get('realtime')
            or {})

        merge_dicts(
            dict1=historic,
            dict2=realtime,
            force=True)

        value = historic | {
            '_source': fetch}

        source[unique] = value


    _source = sorted(
        source.items())

    return dict(_source)



def merge_find(  # noqa: CFQ004
    merge: UbiqMerge,
    kind: Optional['HomieKinds'] = None,
    unique: Optional[str] = None,
    label: Optional[str] = None,
) -> list[DictStrAny]:
    """
    Return the content related to the item in parent system.

    :param merge: Dictionary from the origin to be updated.
    :param kind: Which kind of Homie object will be located.
    :param unique: Unique identifier within parents system.
    :param label: Friendly name or label within the parent.
    :returns: Content related to the item in parent system.
    """

    assert unique or label

    if label is not None:
        label = strplwr(label)

    if unique is not None:
        unique = strplwr(unique)

    found: list[DictStrAny] = []


    if kind is not None:
        assert kind == 'device'


    def _match_unique() -> bool:

        if unique is None:
            return True

        uniques = [
            value.get('_id'),
            value.get('last_ip'),
            value.get('mac')]

        uniques = [
            strplwr(x)
            for x in uniques
            if x is not None]

        return unique in uniques


    def _match_label() -> bool:

        if label is None:
            return True

        if 'name' not in value:
            return NCFalse

        _label = strplwr(
            value['name'])

        return label == _label


    values = merge.values()

    for value in values:

        if not _match_unique():
            continue

        if not _match_label():
            continue

        found.append(value)


    return found
