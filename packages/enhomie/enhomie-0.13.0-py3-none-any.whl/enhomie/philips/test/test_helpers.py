"""
Functions and routines associated with Enasis Network Homie Automate.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from typing import TYPE_CHECKING

from pytest import raises

from ..helpers import request_action
from ..origin import PhueOrigin
from ...utils import Idempotent

if TYPE_CHECKING:
    from ...homie import Homie
    from ...utils import TestBodies



def test_request_action(  # noqa: CFQ001
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
    devices = childs.devices
    groups = childs.groups
    scenes = childs.scenes

    scene1 = scenes['active']
    scene2 = scenes['standby']


    planets = bodies.planets
    moons = dict(bodies.moons)

    for planet in planets:

        moon = moons[planet]

        origin = origins[
            f'{planet}_philips']

        assert isinstance(
            origin, PhueOrigin)

        light = devices[
            f'{planet}_light1']

        group = groups[moon]

        assert origin.refresh()


        request_action(
            origin=origin,
            target=group,
            scene=scene1)

        with raises(Idempotent):

            request_action(
                origin=origin,
                target=group,
                scene=scene2)

        request_action(
            origin=origin,
            target=group,
            scene=scene1,
            change=False)


        request_action(
            origin=origin,
            target=light,
            scene=scene1)

        with raises(Idempotent):

            request_action(
                origin=origin,
                target=light,
                scene=scene2)

        request_action(
            origin=origin,
            target=light,
            scene=scene1,
            change=False)


        request_action(
            origin=origin,
            target=light,
            state='nopower')

        with raises(Idempotent):

            request_action(
                origin=origin,
                target=light,
                state='poweron')

        request_action(
            origin=origin,
            target=light,
            state='nopower',
            change=False)


        request_action(
            origin=origin,
            target=group,
            state='nopower')

        with raises(Idempotent):

            request_action(
                origin=origin,
                target=group,
                state='poweron')

        request_action(
            origin=origin,
            target=group,
            state='nopower',
            change=False)


        request_action(
            origin=origin,
            target=light,
            color='ff00cc')

        with raises(Idempotent):

            request_action(
                origin=origin,
                target=light,
                color='003333')

        request_action(
            origin=origin,
            target=light,
            color='ff00cc',
            change=False)


        request_action(
            origin=origin,
            target=group,
            color='ff00cc')

        with raises(Idempotent):

            request_action(
                origin=origin,
                target=group,
                color='003333')

        request_action(
            origin=origin,
            target=group,
            color='ff00cc',
            change=False)


        request_action(
            origin=origin,
            target=light,
            level=100)

        with raises(Idempotent):

            request_action(
                origin=origin,
                target=light,
                level=80)

        request_action(
            origin=origin,
            target=light,
            level=100,
            change=False)


        request_action(
            origin=origin,
            target=group,
            level=100)

        with raises(Idempotent):

            request_action(
                origin=origin,
                target=group,
                level=80)

        request_action(
            origin=origin,
            target=group,
            level=100,
            change=False)
