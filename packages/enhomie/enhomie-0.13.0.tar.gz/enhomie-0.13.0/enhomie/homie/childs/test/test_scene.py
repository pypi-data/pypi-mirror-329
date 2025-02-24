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



def test_HomieScene(
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
    scenes = childs.scenes


    scene = scenes['standby']


    attrs = lattrs(scene)

    assert attrs == [
        '_HomieChild__homie',
        '_HomieChild__name',
        '_HomieChild__params']


    assert inrepr(
        'scene.HomieScene',
        scene)

    assert isinstance(
        hash(scene), int)

    assert instr(
        'scene.HomieScene',
        scene)


    scene.validate()

    assert scene.homie

    assert scene.name == 'standby'

    assert scene.family == 'builtins'

    assert scene.kind == 'scene'

    assert scene.params

    assert scene.dumped

    assert scene.stage()


    planets = bodies.planets

    for planet in planets:

        origin = origins[
            f'{planet}_philips']

        origin.refresh()

        assert scene.source(origin)


        device = devices[
            f'{planet}_light1']

        stage1, stage2 = (
            scene.stage(device),
            scene.stage())

        assert stage1 == stage2


        device = devices[
            f'{planet}_light2']

        stage1, stage2 = (
            scene.stage(device),
            scene.stage())

        assert stage1 != stage2
