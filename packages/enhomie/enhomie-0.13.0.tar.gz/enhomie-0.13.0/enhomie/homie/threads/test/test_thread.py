"""
Functions and routines associated with Enasis Network Homie Automate.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from typing import TYPE_CHECKING

from encommon.times import Time

if TYPE_CHECKING:
    from ...service import HomieService
    from ....utils import TestBodies



def test_HomieThread_cover(
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

    assert service.actions

    member = service.actions
    threads = member.threads


    planets = bodies.planets

    for planet in planets:

        origin = origins[
            f'{planet}_philips']

        thread = threads[
            f'{planet}_philips']


        assert origin.refresh()

        uitem = origin.get_update()

        expired = (
            thread.expired(uitem))

        assert expired is False

        uitem.time = Time('-1h')

        expired = (
            thread.expired(uitem))

        assert expired is True
