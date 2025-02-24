"""
Functions and routines associated with Enasis Network Homie Automate.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from pathlib import Path
from typing import TYPE_CHECKING

from encommon.types import DictStrAny
from encommon.types import inrepr
from encommon.types import instr
from encommon.types import lattrs
from encommon.utils import save_text

from respx import MockRouter

from ..aspired import HomieAspiredItem
from ....conftest import config_factory
from ....conftest import homie_factory

if TYPE_CHECKING:
    from ...homie import Homie
    from ....utils import TestBodies



def test_HomieAspiredItem(
    homie: 'Homie',
) -> None:
    """
    Perform various tests associated with relevant routines.

    :param homie: Primary class instance for Homie Automate.
    """

    childs = homie.childs
    devices = childs.devices
    groups = childs.groups
    aspires = childs.aspires

    device = devices[
        'jupiter_light1']

    group1 = groups['ganymede']
    group2 = groups['halimede']

    aspire = aspires[
        'jupiter_active']

    model = HomieAspiredItem


    item = model(
        group1, aspire)


    attrs = lattrs(item)

    assert attrs == [
        'target',
        'aspire',
        'state',
        'color',
        'level',
        'scene']


    assert item.target

    assert item.aspire

    assert item.state == 'poweron'

    assert not item.color

    assert item.level == 100

    assert item.scene


    item1 = model(
        group2, aspire)

    item2 = model(
        device, aspire)


    assert item < item1
    assert item < item2



def test_HomieAspired(
    homie: 'Homie',
    bodies: 'TestBodies',
) -> None:
    """
    Perform various tests associated with relevant routines.

    :param homie: Primary class instance for Homie Automate.
    :param bodies: Locations and groups for use in testing.
    """

    childs = homie.childs
    origins = childs.origins


    aspired = homie.aspired


    attrs = lattrs(aspired)

    assert attrs == [
        '_HomieAspired__homie']


    assert inrepr(
        'aspired.HomieAspired',
        aspired)

    assert isinstance(
        hash(aspired), int)

    assert instr(
        'aspired.HomieAspired',
        aspired)


    assert homie.refresh()


    planets = bodies.planets

    total = 0

    event = {'foo': 'bar'}

    for planet in planets:

        origin = origins[
            f'{planet}_philips']

        sitem = (
            origin
            .get_stream(event))

        aitems = (
            aspired.items(sitem))

        total += len(aitems)

        if len(aitems) == 0:
            break

        assert len(aitems) == 4

    assert total == 4



def test_HomieAspired_cover(
    tmp_path: Path,
    respx_mock: MockRouter,
    replaces: DictStrAny,
    bodies: 'TestBodies',
) -> None:
    """
    Perform various tests associated with relevant routines.

    :param tmp_path: pytest object for temporal filesystem.
    :param respx_mock: Object for mocking request operation.
    :param replaces: Mapping of what to replace in samples.
    :param bodies: Locations and groups for use in testing.
    """

    samples = (
        tmp_path / 'homie')

    samples.mkdir()

    save_text(
        samples / 'test.yml',
        """
        aspires:
         pytest:
          pause: 1
          occurs:
          - builtins_regexp:
             patterns: '.*'
        """)  # noqa: LIT003

    homie = homie_factory(
        config_factory(tmp_path),
        respx_mock=respx_mock)


    childs = homie.childs
    origins = childs.origins
    aspired = homie.aspired


    assert homie.refresh()


    planets = bodies.planets

    event = {'foo': 'bar'}

    for planet in planets:

        origin = origins[
            f'{planet}_philips']

        sitem = (
            origin
            .get_stream(event))

        aitems = (
            aspired.items(sitem))

        if len(aitems) == 0:
            break

        assert len(aitems) == 4
