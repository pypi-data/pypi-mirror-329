"""
Functions and routines associated with Enasis Network Homie Automate.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from typing import TYPE_CHECKING

from ..action import HubiAction
from ..action import HubiActionItem

if TYPE_CHECKING:
    from ...homie import HomieService
    from ...utils import TestBodies



def test_HubiAction_cover(
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

    assert service.actions

    actions = service.actions
    threads = actions.threads


    planets = bodies.planets

    for planet in planets:

        origin = origins[
            f'{planet}_hubitat']

        device = devices[
            f'{planet}_light2']

        thread = threads[
            f'{planet}_hubitat']

        assert isinstance(
            thread, HubiAction)

        model = HubiActionItem


        aitem = model(
            origin, device)

        aitem.device = None

        thread.execute(aitem)
