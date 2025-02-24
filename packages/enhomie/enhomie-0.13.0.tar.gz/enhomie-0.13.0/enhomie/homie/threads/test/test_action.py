"""
Functions and routines associated with Enasis Network Homie Automate.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from typing import TYPE_CHECKING

from encommon.types import inlist
from encommon.types import inrepr
from encommon.types import instr
from encommon.types import lattrs

from pytest import raises

from ..action import HomieActionItem

if TYPE_CHECKING:
    from ...service import HomieService
    from ....utils import TestBodies



def test_HomieActionItem(
    service: 'HomieService',
    bodies: 'TestBodies',
) -> None:
    """
    Perform various tests associated with relevant routines.

    :param service: Ancilary Homie Automate class instance.
    :param bodies: Locations and groups for use in testing.
    """

    homie = service.homie
    childs = homie.childs
    origins = childs.origins
    devices = childs.devices
    groups = childs.groups
    scenes = childs.scenes

    model = HomieActionItem


    moons = (
        dict(bodies.moons)
        .items())

    for planet, moon in moons:

        origin = origins[
            f'{planet}_philips']

        device = devices[
            f'{planet}_light1']

        group = groups[moon]
        scene = scenes['active']


        item = model(
            origin, group,
            color='ff00cc')


        attrs = lattrs(item)

        assert attrs == [
            'group',
            'state',
            'color',
            'level',
            'scene',
            'origin',
            'time']


        assert inrepr(
            'HomieActionItem',
            item)

        with raises(TypeError):
            hash(item)

        assert instr(
            'HomieActionItem',
            item)


        assert item.time.since > 0

        assert item.origin == origin.name

        assert item.group == group.name

        assert not item.device

        assert not item.state

        assert item.color == 'ff00cc'

        assert not item.level


        item = model(
            origin, device,
            scene=scene)

        assert not item.group

        assert item.device == device.name

        assert item.scene == scene.name



def test_HomieAction(
    service: 'HomieService',
    bodies: 'TestBodies',
) -> None:
    """
    Perform various tests associated with relevant routines.

    :param service: Ancilary Homie Automate class instance.
    :param bodies: Locations and groups for use in testing.
    """

    assert service.actions

    member = service.actions
    threads = member.threads


    planets = bodies.planets

    for planet in planets:

        thread = threads[
            f'{planet}_philips']


        attrs = lattrs(thread)

        # Inherits Thread class

        assert inlist(
            '_HomieThread__member',
            attrs)

        assert inlist(
            '_HomieThread__origin',
            attrs)

        assert inlist(
            '_HomieThread__aqueue',
            attrs)

        assert inlist(
            '_HomieThread__uqueue',
            attrs)

        assert inlist(
            '_HomieThread__squeue',
            attrs)


        assert inrepr(
            'Action(PhueAction',
            thread)

        assert isinstance(
            hash(thread), int)

        assert instr(
            'Action(PhueAction',
            thread)


        assert thread.homie

        assert thread.member

        assert thread.origin

        assert thread.aqueue

        assert thread.uqueue

        assert thread.squeue

        assert not thread.congest

        assert not thread.enqueue
