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
    from ....utils import TestTimes
    from ....utils import TestBodies



def test_HomieDesire(
    homie: 'Homie',
    bodies: 'TestBodies',
    times: 'TestTimes',
) -> None:
    """
    Perform various tests associated with relevant routines.

    :param homie: Primary class instance for Homie Automate.
    :param bodies: Locations and groups for use in testing.
    :param times: Times that are used with tests in project.
    """

    childs = homie.childs
    desires = childs.desires


    planets = bodies.planets

    for planet in planets:

        name = f'{planet}_active'

        desire = desires[name]


        attrs = lattrs(desire)

        assert attrs == [
            '_HomieChild__homie',
            '_HomieChild__name',
            '_HomieChild__params',
            '_HomieDesire__wheres',
            '_HomieDesire__timers']


        assert inrepr(
            'desire.HomieDesire',
            desire)

        assert isinstance(
            hash(desire), int)

        assert instr(
            'desire.HomieDesire',
            desire)


        desire.validate()

        assert desire.homie

        assert desire.name == name

        assert desire.family == 'builtins'

        assert desire.kind == 'desire'

        assert desire.params

        assert desire.weight == 0

        assert len(desire.devices) == 1

        assert len(desire.groups) == 1

        assert len(desire.wheres) == 5

        assert desire.paused(
            desire.devices[0])

        assert desire.dumped



def test_HomieDesires_cover(
    tmp_path: Path,
    respx_mock: MockRouter,
    times: 'TestTimes',
) -> None:
    """
    Perform various tests associated with relevant routines.

    :param tmp_path: pytest object for temporal filesystem.
    :param respx_mock: Object for mocking request operation.
    :param times: Times that are used with tests in project.
    """

    samples = (
        tmp_path / 'homie')

    samples.mkdir()

    save_text(
        samples / 'test.yml',
        """
        desires:
         pytest:
          store:
          - unique: desire
            value: true
            expire: '1y'
        """)  # noqa: LIT003

    homie = homie_factory(
        config_factory(tmp_path),
        respx_mock=respx_mock)


    childs = homie.childs

    desire = (
        childs.desires
        ['pytest'])


    assert not desire.devices

    assert not desire.groups


    time = times.middle

    assert not (
        desire.when(time))
