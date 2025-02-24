"""
Functions and routines associated with Enasis Network Homie Automate.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from typing import TYPE_CHECKING

from ..helpers import ubiq_latest
from ...origin import UbiqOrigin

if TYPE_CHECKING:
    from ....homie import Homie
    from ....utils import TestBodies



def test_ubiq_latest(
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


    planets = bodies.planets

    for planet in planets:

        origin = origins[
            f'{planet}_ubiquiti']

        assert isinstance(
            origin, UbiqOrigin)

        assert origin.refresh()


        assert origin.merge

        values = (
            origin.merge
            .values())


        for value in values:

            latest = ubiq_latest(value)

            assert latest > '-2d'
