"""
Functions and routines associated with Enasis Network Homie Automate.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from copy import deepcopy
from json import dumps
from typing import Literal
from typing import Optional
from typing import TYPE_CHECKING
from urllib.parse import quote_plus

from encommon.colors import Color
from encommon.types import DictStrAny
from encommon.types import getate
from encommon.types import strplwr

from httpx import Response

from .device import HubiDevice
from ..utils import Idempotent
from ..utils import UnexpectedCondition

if TYPE_CHECKING:
    from .origin import HubiOrigin
    from ..homie.common import HomieKinds
    from ..homie.common import HomieState
    from ..homie.childs import HomieScene
    from ..homie.threads import HomieActionNode



HubiFetch = list[DictStrAny]
HubiMerge = dict[str, DictStrAny]



_RESPONSE = Optional[
    Response | Literal[True]]

_APROPS = Literal[
    'state',
    'color',
    'level']

_ASTATES = Literal[
    'on', 'off']

_AVALUES = Optional[
    _ASTATES
    | int | Color]



def merge_fetch(
    fetch: HubiFetch,
) -> HubiMerge:
    """
    Return the content related to the item in parent system.

    :param fetch: Dictionary from the origin to be updated.
    :returns: Content related to the item in parent system.
    """

    fetch = deepcopy(fetch)

    source = {
        x['id']: x
        for x in fetch}

    _source = sorted(
        source.items())

    return dict(_source)



def merge_find(  # noqa: CFQ004
    merge: HubiMerge,
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


    def _match_kind() -> bool:

        if kind is None:
            return True

        _kind: Optional[str] = None

        _capas = value[
            'capabilities']

        if 'Light' in _capas:
            _kind = 'device'

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

        _label = strplwr(
            value['label'])

        return label == _label


    values = merge.values()

    for value in values:

        if not _match_kind():
            continue

        if not _match_unique():
            continue

        if not _match_label():
            continue

        found.append(value)


    return found



def request_action(  # noqa: CFQ001,CFQ002,CFQ004
    origin: 'HubiOrigin',
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

    assert kind == 'device'

    changed: set[bool] = set()


    source = target.source


    if scene is not None:

        assert isinstance(
            target, HubiDevice)

        stage = (
            scene
            .stage(target))

        if state is None:
            state = stage.state

        if color is None:
            color = stage.color

        if level is None:
            level = stage.level


    assert source is not None

    unique = source['id']


    _state: _AVALUES = (
        'off'
        if state == 'nopower'
        else 'on')


    if isinstance(color, str):
        color = Color(color)


    def _set_state() -> None:

        response = request(
            origin=origin,
            unique=unique,
            property='state',
            value=_state,
            force=force,
            change=change,
            timeout=timeout)

        if response is None:
            return None

        changed.add(True)

        if (change is False
                or homie.dryrun):
            return None

        assert isinstance(
            response, Response)

        (response
         .raise_for_status())


    def _set_color() -> None:

        response = request(
            origin=origin,
            unique=unique,
            property='color',
            value=color,
            force=force,
            change=change,
            timeout=timeout)

        if response is None:
            return None

        changed.add(True)

        if (change is False
                or homie.dryrun):
            return None

        assert isinstance(
            response, Response)

        (response
         .raise_for_status())


    def _set_level() -> None:

        response = request(
            origin=origin,
            unique=unique,
            property='level',
            value=level,
            force=force,
            change=change,
            timeout=timeout)

        if response is None:
            return None

        changed.add(True)

        if (change is False
                or homie.dryrun):
            return None

        assert isinstance(
            response, Response)

        (response
         .raise_for_status())


    if state is not None:
        _set_state()

    if state != 'nopower':

        if color is not None:
            _set_color()

        if level is not None:
            _set_level()


    if not any(changed):
        raise Idempotent



def action_request(  # noqa: CFQ001,CFQ002,CFQ004
    origin: 'HubiOrigin',
    unique: str,
    *,
    property: _APROPS,
    value: _AVALUES = None,
    force: bool = False,
    change: bool = True,
    timeout: Optional[int] = None,
) -> _RESPONSE:
    """
    Request to execute the action on target from the bridge.

    :param origin: Child class instance for Homie Automate.
    :param type: Which type of target to perform the action.
    :param unique: Unique identifier within parents system.
    :param property: What attribute on the target is change.
    :param value: Value relating to property being updated.
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


    def _get_attr(
        attr: str,
    ) -> str:

        pre = 'attributes'

        key = (
            'saturation'
            if attr == 'sat'
            else attr)

        value = getate(
            merge,
            f'{pre}/{key}')

        return str(value)


    def _set_state() -> _RESPONSE:

        assert isinstance(
            value, str)

        crrnt = _get_attr('switch')

        path = (
            f'devices/{unique}'
            f'/{value}')

        if (crrnt == value
                and not force):
            return None

        if (change is False
                or homie.dryrun):
            return True

        return request(
            method='get',
            path=path,
            timeout=timeout)


    def _set_color() -> _RESPONSE:

        assert isinstance(
            value, Color)

        hsl = list(value.hsl)

        hsb = (
            int(hsl[0] / 3.6),
            int(hsl[1]))

        hue = _get_attr('hue')

        sat = _get_attr('sat')

        eulav = {
            'hue': hsb[0],
            'saturation': hsb[1]}

        crrnt = {
            'hue': int(hue),
            'saturation': int(sat)}

        if (crrnt == eulav
                and not force):
            return None


        quote = quote_plus(
            dumps(eulav))

        path = (
            f'devices/{unique}'
            f'/setColor/{quote}')

        if (change is False
                or homie.dryrun):
            return True

        return request(
            method='get',
            path=path,
            timeout=timeout)


    def _set_level() -> _RESPONSE:

        assert isinstance(
            value, int | float)

        path = (
            f'devices/{unique}'
            f'/setLevel/{value}')

        crrnt = _get_attr('level')

        if (crrnt == str(value)
                and not force):
            return None

        if (change is False
                or homie.dryrun):
            return True

        return request(
            method='get',
            path=path,
            timeout=timeout)


    if property == 'state':
        return _set_state()

    if property == 'color':
        return _set_color()

    if property == 'level':
        return _set_level()


    raise UnexpectedCondition
