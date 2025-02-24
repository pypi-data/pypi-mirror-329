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



def test_HomieAspire(
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

        name = f'{planet}_active'

        aspire = aspires[name]


        attrs = lattrs(aspire)

        assert attrs == [
            '_HomieChild__homie',
            '_HomieChild__name',
            '_HomieChild__params',
            '_HomieAspire__occurs',
            '_HomieAspire__wheres',
            '_HomieAspire__timer']


        assert inrepr(
            'aspire.HomieAspire',
            aspire)

        assert isinstance(
            hash(aspire), int)

        assert instr(
            'aspire.HomieAspire',
            aspire)


        aspire.validate()

        assert aspire.homie

        assert aspire.name == name

        assert aspire.family == 'builtins'

        assert aspire.kind == 'aspire'

        assert aspire.params

        assert len(aspire.devices) == 1

        assert len(aspire.groups) == 1

        assert len(aspire.occurs) == 6

        assert len(aspire.wheres) == 1

        assert not aspire.paused

        assert aspire.dumped



def test_HomieAspire_cover(
    tmp_path: Path,
    respx_mock: MockRouter,
    bodies: 'TestBodies',
) -> None:
    """
    Perform various tests associated with relevant routines.

    :param tmp_path: pytest object for temporal filesystem.
    :param respx_mock: Object for mocking request operation.
    :param bodies: Locations and groups for use in testing.
    """

    samples = (
        tmp_path / 'homie')

    samples.mkdir()

    save_text(
        samples / 'test.yml',
        """
        aspires:
         pytest:
          store:
          - unique: aspire
            value: true
            expire: '1y'
        """)  # noqa: LIT003

    homie = homie_factory(
        config_factory(tmp_path),
        respx_mock=respx_mock)


    childs = homie.childs
    origins = childs.origins

    aspire = (
        childs.aspires
        ['pytest'])


    assert not aspire.devices

    assert not aspire.groups


    planets = bodies.planets

    event = {'foo': 'bar'}

    for planet in planets:

        origin = origins[
            f'{planet}_philips']

        sitem = (
            origin
            .get_stream(event))

        assert not (
            aspire.when(sitem))
