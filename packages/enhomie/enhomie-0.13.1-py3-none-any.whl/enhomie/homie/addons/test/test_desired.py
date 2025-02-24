"""
Functions and routines associated with Enasis Network Homie Automate.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from pathlib import Path
from time import sleep as block_sleep
from typing import TYPE_CHECKING

from encommon.types import DictStrAny
from encommon.types import inrepr
from encommon.types import instr
from encommon.types import lattrs
from encommon.utils import save_text

from respx import MockRouter

from ..desired import HomieDesiredItem
from ....conftest import config_factory
from ....conftest import homie_factory

if TYPE_CHECKING:
    from ...homie import Homie
    from ....utils import TestTimes



def test_HomieDesiredItem(
    homie: 'Homie',
) -> None:
    """
    Perform various tests associated with relevant routines.

    :param homie: Primary class instance for Homie Automate.
    """

    childs = homie.childs
    devices = childs.devices
    groups = childs.groups
    desires = childs.desires

    device = devices[
        'jupiter_light1']

    group1 = groups['ganymede']
    group2 = groups['halimede']

    desire = desires[
        'jupiter_active']

    model = HomieDesiredItem


    item = model(
        group1, desire)


    attrs = lattrs(item)

    assert attrs == [
        'target',
        'weight',
        'desire',
        'state',
        'color',
        'level',
        'scene']


    assert item.target

    assert item.desire

    assert item.state == 'poweron'

    assert not item.color

    assert item.level == 100

    assert item.scene


    item1 = model(
        group2, desire)

    item2 = model(
        device, desire)


    assert item < item1
    assert item < item2



def test_HomieDesired(
    homie: 'Homie',
    times: 'TestTimes',
) -> None:
    """
    Perform various tests associated with relevant routines.

    :param homie: Primary class instance for Homie Automate.
    :param times: Times that are used with tests in project.
    """


    desired = homie.desired


    attrs = lattrs(desired)

    assert attrs == [
        '_HomieDesired__homie']


    assert inrepr(
        'desired.HomieDesired',
        desired)

    assert isinstance(
        hash(desired), int)

    assert instr(
        'desired.HomieDesired',
        desired)


    assert homie.refresh()


    time = times.middle

    aitems = (
        desired.items(time))

    assert len(aitems) == 0

    block_sleep(1.1)

    aitems = (
        desired.items(time))

    assert len(aitems) == 4



def test_HomieDesired_cover(
    tmp_path: Path,
    respx_mock: MockRouter,
    replaces: DictStrAny,
    times: 'TestTimes',
) -> None:
    """
    Perform various tests associated with relevant routines.

    :param tmp_path: pytest object for temporal filesystem.
    :param respx_mock: Object for mocking request operation.
    :param replaces: Mapping of what to replace in samples.
    :param times: Times that are used with tests in project.
    """

    samples = (
        tmp_path / 'homie')

    samples.mkdir()

    save_text(
        samples / 'test.yml',
        """
        desires:
         pytest:
          wheres:
          - builtins_period:
             start: '00:00'
        """)  # noqa: LIT003

    homie = homie_factory(
        config_factory(tmp_path),
        respx_mock=respx_mock)


    desired = homie.desired


    assert homie.refresh()


    time = times.middle

    aitems = (
        desired.items(time))

    assert len(aitems) == 0

    block_sleep(1.1)

    aitems = (
        desired.items(time))

    assert len(aitems) == 4
