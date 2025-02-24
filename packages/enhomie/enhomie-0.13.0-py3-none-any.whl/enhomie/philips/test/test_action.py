"""
Functions and routines associated with Enasis Network Homie Automate.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from typing import TYPE_CHECKING

from ..action import PhueAction
from ..action import PhueActionItem

if TYPE_CHECKING:
    from ...homie import HomieService
    from ...utils import TestBodies



def test_PhueAction_cover(
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

    assert service.actions

    actions = service.actions
    threads = actions.threads

    model = PhueActionItem


    planets = bodies.planets
    moons = dict(bodies.moons)

    for planet in planets:

        moon = moons[planet]

        origin = origins[
            f'{planet}_philips']

        device = devices[
            f'{planet}_light1']

        group = groups[moon]

        assert origin.refresh()

        thread = threads[
            f'{planet}_philips']

        assert isinstance(
            thread, PhueAction)


        aitem = model(
            origin, device)

        thread.execute(aitem)


        aitem.device = None

        thread.execute(aitem)


        aitem = model(
            origin, group)

        group.params.origin = None

        thread.execute(aitem)
