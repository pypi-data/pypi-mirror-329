"""
Functions and routines associated with Enasis Network Homie Automate.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from typing import TYPE_CHECKING

from ..update import UbiqUpdateItem

if TYPE_CHECKING:
    from ...homie import HomieService
    from ...utils import TestBodies



def test_UbiqUpdateItem(
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

    model = UbiqUpdateItem


    planets = bodies.planets

    fetch = {'foo': 'bar'}

    for planet in planets:

        origin = origins[
            f'{planet}_ubiquiti']


        item = model(
            origin, fetch)


        assert item.origin == origin.name

        assert item.fetch == fetch
