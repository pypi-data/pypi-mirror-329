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

from ..update import HomieUpdateItem

if TYPE_CHECKING:
    from ...service import HomieService
    from ....utils import TestBodies



def test_HomieUpdateItem(
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


    planets = bodies.planets

    model = HomieUpdateItem

    for planet in planets:

        origin = origins[
            f'{planet}_philips']


        item = model(origin)


        attrs = lattrs(item)

        assert attrs == [
            'origin',
            'time']


        assert inrepr(
            'HomieUpdateItem',
            item)

        with raises(TypeError):
            hash(item)

        assert instr(
            'HomieUpdateItem',
            item)


        assert item.time.since > 0

        assert item.origin == origin.name



def test_HomieUpdate(
    service: 'HomieService',
    bodies: 'TestBodies',
) -> None:
    """
    Perform various tests associated with relevant routines.

    :param service: Ancilary Homie Automate class instance.
    :param bodies: Locations and groups for use in testing.
    """

    assert service.updates

    member = service.updates
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


        assert inrepr(
            'Update(PhueUpdate',
            thread)

        assert isinstance(
            hash(thread), int)

        assert instr(
            'Update(PhueUpdate',
            thread)


        assert thread.homie

        assert thread.member

        assert thread.origin

        assert thread.aqueue

        assert thread.uqueue

        assert thread.squeue

        assert not thread.congest

        assert not thread.enqueue
