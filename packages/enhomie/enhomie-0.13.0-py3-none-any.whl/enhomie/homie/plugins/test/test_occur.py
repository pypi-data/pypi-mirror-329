"""
Functions and routines associated with Enasis Network Homie Automate.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from typing import TYPE_CHECKING

from encommon.types import inrepr
from encommon.types import instr
from encommon.types import lattrs

if TYPE_CHECKING:
    from ...homie import Homie
    from ....utils import TestBodies



def test_HomieOccur(
    homie: 'Homie',
    bodies: 'TestBodies',
) -> None:
    """
    Perform various tests associated with relevant routines.

    :param homie: Primary class instance for Homie Automate.
    :param bodies: Locations and groups for use in testing.
    """

    childs = homie.childs
    aspires = childs.aspires


    planets = bodies.planets

    for planet in planets:

        aspire = aspires[
            f'{planet}_active']

        occurs = aspire.occurs


        plugin = occurs[0]


        attrs = lattrs(plugin)

        assert attrs == [
            '_HomiePlugin__homie',
            '_HomiePlugin__params',
            '_HomiePlugin__drivers']


        assert inrepr(
            'occur.HomieOccur',
            plugin)

        assert isinstance(
            hash(plugin), int)

        assert instr(
            'occur.HomieOccur',
            plugin)


        plugin.validate()

        assert plugin.homie

        assert plugin.family == 'builtins'

        assert plugin.kind == 'occur'

        assert plugin.params

        assert len(plugin.drivers) == 1
