"""
Functions and routines associated with Enasis Network Homie Automate.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from typing import TYPE_CHECKING

from encommon.types import inrepr
from encommon.types import instr
from encommon.types import lattrs

from ..regexp import DriverBltnRegexp

if TYPE_CHECKING:
    from ...homie import Homie
    from ...utils import TestBodies



def test_DriverBltnRegexp(
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
    aspires = childs.aspires


    assert homie.refresh()


    planets = bodies.planets

    family = 'builtins'

    event = {'foo': 'bar'}

    for planet in planets:

        origin = origins[
            f'{planet}_philips']

        aspire = aspires[
            f'{planet}_active']

        driver = (
            aspire.occurs[5]
            .drivers[0])

        assert isinstance(
            driver, DriverBltnRegexp)


        attrs = lattrs(driver)

        assert attrs == [
            '_HomieDriver__plugin',
            '_HomieDriver__params']


        assert inrepr(
            'regexp.DriverBltnRegexp',
            driver)

        assert isinstance(
            hash(driver), int)

        assert instr(
            'regexp.DriverBltnRegexp',
            driver)


        driver.validate()

        assert driver.plugin

        assert driver.family == family

        assert driver.kinds == ['occur']

        assert driver.params


        sitem = (
            origin
            .get_stream(event))

        assert driver.occur(sitem)
