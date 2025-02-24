"""
Functions and routines associated with Enasis Network Homie Automate.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from typing import TYPE_CHECKING

from encommon.types import lattrs

from ..device import PhueDevice

if TYPE_CHECKING:
    from ...homie import Homie
    from ...utils import TestBodies



def test_PhueDevice(
    homie: 'Homie',
    bodies: 'TestBodies',
) -> None:
    """
    Perform various tests associated with relevant routines.

    :param homie: Primary class instance for Homie Automate.
    :param bodies: Locations and groups for use in testing.
    """

    childs = homie.childs
    devices = childs.devices


    planets = bodies.planets

    family = 'philips'

    for planet in planets:

        name = f'{planet}_light1'

        device = devices[name]

        assert isinstance(
            device, PhueDevice)


        attrs = lattrs(device)

        assert attrs == [
            '_HomieChild__homie',
            '_HomieChild__name',
            '_HomieChild__params']


        device.validate()

        assert device.homie

        assert device.name == name

        assert device.family == family

        assert device.kind == 'device'

        assert device.origin

        assert device.params

        assert not device.source

        assert device.dumped


        device.origin.refresh()

        assert device.source
