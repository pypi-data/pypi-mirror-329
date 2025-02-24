"""
Functions and routines associated with Enasis Network Homie Automate.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from copy import deepcopy
from typing import Literal
from typing import Optional
from typing import TYPE_CHECKING

from encommon.colors import Color
from encommon.types import DictStrAny
from encommon.types import NCFalse
from encommon.types import NCNone
from encommon.types import getate
from encommon.types import setate
from encommon.types import strplwr

from httpx import Response

from .device import PhueDevice
from ..utils import Idempotent

if TYPE_CHECKING:
    from .origin import PhueOrigin
    from ..homie.common import HomieKinds
    from ..homie.common import HomieState
    from ..homie.childs import HomieScene
    from ..homie.threads import HomieActionNode



PhueFetch = DictStrAny
PhueMerge = dict[str, PhueFetch]



_RESPONSE = Optional[
    Response | Literal[True]]

_APROPS = Literal[
    'state',
    'color',
    'level']

_ATYPES = Literal[
    'scene',
    'grouped_light',
    'light']

_ASTATES = Literal[
    'on', 'off',
    'active']

_AVALUES = Optional[
    _ASTATES
    | int | Color]



def merge_fetch(
    fetch: PhueFetch,
) -> PhueMerge:
    """
    Return the content related to the item in parent system.

    :param fetch: Dictionary from the origin to be updated.
    :returns: Content related to the item in parent system.
    """

    fetch = deepcopy(fetch)

    source = {
        x['id']: x for x
        in fetch['data']}

    origin = deepcopy(source)


    def _enrichment() -> None:

        rtype = item['rtype']
        rid = item['rid']

        if 'taurus_' in rtype:
            return None

        item['_source'] = (
            origin[rid])


    items1 = source.items()

    for key, value in items1:

        if 'services' not in value:
            continue

        items2 = value['services']

        for item in items2:
            _enrichment()


    _source = sorted(
        source.items())

    return dict(_source)



def merge_find(  # noqa: CFQ001,CFQ004
    merge: PhueMerge,
    kind: Optional['HomieKinds'] = None,
    unique: Optional[str] = None,
    label: Optional[str] = None,
    relate: Optional['HomieActionNode'] = None,
) -> list[DictStrAny]:
    """
    Return the content related to the item in parent system.

    :param merge: Dictionary from the origin to be updated.
    :param kind: Which kind of Homie object will be located.
    :param unique: Unique identifier within parents system.
    :param label: Friendly name or label within the parent.
    :param relate: Child class instance for Homie Automate.
    :returns: Content related to the item in parent system.
    """

    assert unique or label

    if label is not None:
        label = strplwr(label)

    if unique is not None:
        unique = strplwr(unique)

    found: list[DictStrAny] = []


    def _match_owner() -> bool:

        if relate is None:
            return True

        _source = relate.source

        if _source is None:
            return NCFalse

        _relate = (
            _source['id']
            if relate is not None
            else None)

        owner = getate(
            value, 'owner/rid')

        group = getate(
            value, 'group/rid')

        match = owner or group

        return (
            False  # noqa: SIM211
            if _relate != match
            else True)


    def _match_kind() -> bool:

        if kind is None:
            return True

        _kind = value['type']

        assert isinstance(_kind, str)

        if _kind == 'room':
            _kind = 'group'

        if _kind == 'zone':
            _kind = 'group'

        return kind == _kind


    def _match_unique() -> bool:

        if unique is None:
            return True

        _unique = strplwr(
            value['id'])

        return unique == _unique


    def _match_label() -> bool:

        if label is None:
            return True

        name = getate(
            value,
            'metadata/name')

        if name is None:
            return False

        _label = strplwr(name)

        return label == _label


    values = merge.values()

    for value in values:

        if not _match_owner():
            continue

        if not _match_kind():
            continue

        if not _match_unique():
            continue

        if not _match_label():
            continue

        found.append(value)


    return found



def request_action(  # noqa: CFQ001,CFQ002,CFQ004
    origin: 'PhueOrigin',
    target: 'HomieActionNode',
    *,
    state: Optional['HomieState'] = None,
    color: Optional[str | Color] = None,
    level: Optional[int] = None,
    scene: Optional['HomieScene'] = None,
    force: bool = False,
    change: bool = True,
    timeout: Optional[int] = None,
) -> None:
    """
    Perform the provided action with specified Homie target.

    :param origin: Child class instance for Homie Automate.
    :param target: Device or group settings will be updated.
    :param state: Determine the state related to the target.
    :param color: Determine the color related to the target.
    :param level: Determine the level related to the target.
    :param scene: Determine the scene related to the target.
    :param force: Override the default for full idempotency.
    :param change: Determine whether the change is executed.
    :param timeout: Timeout waiting for the server response.
    """

    homie = origin.homie
    kind = target.kind

    request = action_request

    changed: set[bool] = set()

    source = target.source


    if (scene is not None
            and kind == 'device'):

        assert isinstance(
            target, PhueDevice)

        stage = (
            scene
            .stage(target))

        if state is None:
            state = stage.state

        if color is None:
            color = stage.color

        if level is None:
            level = stage.level


    elif (scene is not None
            and kind == 'group'):

        source = scene.source(
            origin, target)


    assert source is not None


    _state: _ASTATES = (
        'off'
        if state == 'nopower'
        else 'on')


    if isinstance(color, str):
        color = Color(color)


    def _set_scene() -> None:

        unique = source['id']

        response = request(
            origin=origin,
            type='scene',
            unique=unique,
            state='active',
            force=force,
            change=change,
            timeout=timeout)

        if response is None:
            return None

        changed.add(True)

        if change is False:
            return None

        if homie.dryrun:
            return None

        assert isinstance(
            response, Response)

        (response
         .raise_for_status())


    def _set_target(  # noqa: CFQ004
        item: DictStrAny,
    ) -> None:

        rtype = item['rtype']
        rid = item['rid']

        itype: _ATYPES = (
            'grouped_light'
            if kind == 'group'
            else 'light')

        if rtype != itype:
            return None

        response = request(
            origin=origin,
            type=itype,
            unique=rid,
            state=(
                _state
                if state is not None
                else None),
            color=color,
            level=level,
            force=force,
            change=change,
            timeout=timeout)

        if response is None:
            return None

        changed.add(True)

        if change is False:
            return None

        if homie.dryrun:
            return NCNone

        assert isinstance(
            response, Response)

        (response
         .raise_for_status())


    def _set_targets() -> None:

        services = (
            source['services'])

        for item in services:
            _set_target(item)


    if kind == 'device':
        _set_targets()

    elif (kind == 'group'
            and scene is None):
        _set_targets()

    elif kind == 'group':
        _set_scene()


    if not any(changed):
        raise Idempotent



def action_request(  # noqa: CFQ001,CFQ002,CFQ004
    origin: 'PhueOrigin',
    type: _ATYPES,
    unique: str,
    *,
    state: Optional[_ASTATES] = None,
    color: Optional[Color] = None,
    level: Optional[int] = None,
    force: bool = False,
    change: bool = True,
    timeout: Optional[int] = None,
) -> _RESPONSE:
    """
    Request to execute the action on target from the bridge.

    :param origin: Child class instance for Homie Automate.
    :param type: Which type of target to perform the action.
    :param unique: Unique identifier within parents system.
    :param state: Determine the state related to the target.
    :param color: Determine the color related to the target.
    :param level: Determine the level related to the target.
    :param force: Override the default for full idempotency.
    :param change: Determine whether the change is executed.
    :param timeout: Timeout waiting for the server response.
    :returns: Response from upstream request to the server.
    """

    bridge = origin.bridge
    request = bridge.request
    homie = origin.homie

    merge = origin.source(
        unique=unique)

    assert merge is not None


    data: DictStrAny = {}

    path = (
        f'resource/{type}'
        f'/{unique}')


    def _set_scene() -> None:

        if state != 'active':
            return None

        key = 'recall/action'
        value = 'active'

        crrnt = getate(
            merge, 'status/active')

        if (crrnt != 'inactive'
                and not force):
            return None

        setate(data, key, value)


    _set_scene()


    def _set_color() -> None:

        if color is None:
            return None

        key = 'color/xy'

        value = {
            'x': color.xy[0],
            'y': color.xy[1]}

        crrnt = getate(merge, key)

        if (crrnt == value
                and not force):
            return None

        setate(data, key, value)


    _set_color()


    def _set_level() -> None:

        if level is None:
            return None

        key = (
            'dimming/'
            'brightness')

        crrnt = int(
            getate(merge, key))

        if (crrnt == level
                and not force):
            return None

        setate(data, key, level)


    _set_level()


    def _set_state() -> None:

        states = ['on', 'off']

        if state not in states:
            return None

        key = 'on/on'
        value = state == 'on'

        crrnt = getate(merge, key)

        if (crrnt == value
                and not force):
            return None

        setate(data, key, value)


    _set_state()


    if len(data) == 0:
        return None

    if change is False:
        return True

    if homie.dryrun:
        return True


    return request(
        method='put',
        path=path,
        json=data,
        timeout=timeout)
