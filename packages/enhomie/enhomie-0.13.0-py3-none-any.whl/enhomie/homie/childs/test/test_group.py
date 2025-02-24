"""
Functions and routines associated with Enasis Network Homie Automate.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from pathlib import Path
from typing import TYPE_CHECKING

from encommon.types import inrepr
from encommon.types import instr
from encommon.types import lattrs
from encommon.utils import save_text

from respx import MockRouter

from ....conftest import config_factory
from ....conftest import homie_factory

if TYPE_CHECKING:
    from ...homie import Homie
    from ....utils import TestBodies



def test_HomieGroup(
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
    groups = childs.groups


    moons = (
        dict(bodies.moons)
        .items())

    for planet, moon in moons:

        origin = origins[
            f'{planet}_philips']

        group = groups[moon]


        attrs = lattrs(group)

        assert attrs == [
            '_HomieChild__homie',
            '_HomieChild__name',
            '_HomieChild__params']


        assert inrepr(
            'group.HomieGroup',
            group)

        assert isinstance(
            hash(group), int)

        assert instr(
            'group.HomieGroup',
            group)


        group.validate()

        assert group.homie

        assert group.name == moon

        assert group.family == 'builtins'

        assert group.kind == 'group'

        assert group.origin

        assert group.params

        assert not group.source

        assert group.dumped


        assert origin.refresh()

        assert group.source



def test_HomieGroup_cover(
    tmp_path: Path,
    respx_mock: MockRouter,
) -> None:
    """
    Perform various tests associated with relevant routines.

    :param tmp_path: pytest object for temporal filesystem.
    :param respx_mock: Object for mocking request operation.
    """

    samples = (
        tmp_path / 'homie')

    samples.mkdir()

    save_text(
        samples / 'test.yml',
        """
        groups:
         pytest:
          devices:
          - jupiter_special
        """)  # noqa: LIT003

    homie = homie_factory(
        config_factory(tmp_path),
        respx_mock=respx_mock)


    childs = homie.childs

    group = (
        childs.groups
        ['pytest'])

    assert not group.source
