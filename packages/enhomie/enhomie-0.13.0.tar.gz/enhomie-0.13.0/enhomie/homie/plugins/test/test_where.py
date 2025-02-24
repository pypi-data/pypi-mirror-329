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



def test_HomieWhere(
    homie: 'Homie',
    bodies: 'TestBodies',
) -> None:
    """
    Perform various tests associated with relevant routines.

    :param homie: Primary class instance for Homie Automate.
    :param bodies: Locations and groups for use in testing.
    """

    childs = homie.childs
    desires = childs.desires


    planets = bodies.planets

    for planet in planets:

        desire = desires[
            f'{planet}_active']

        wheres = desire.wheres


        plugin = wheres[0]


        attrs = lattrs(plugin)

        assert attrs == [
            '_HomiePlugin__homie',
            '_HomiePlugin__params',
            '_HomiePlugin__drivers']


        assert inrepr(
            'where.HomieWhere',
            plugin)

        assert isinstance(
            hash(plugin), int)

        assert instr(
            'where.HomieWhere',
            plugin)


        plugin.validate()

        assert plugin.homie

        assert plugin.family == 'builtins'

        assert plugin.kind == 'where'

        assert plugin.params

        assert len(plugin.drivers) == 1
