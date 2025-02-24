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

from ..change import DriverPhueChange
from ....conftest import config_factory
from ....conftest import homie_factory

if TYPE_CHECKING:
    from ....homie import Homie
    from ....utils import TestBodies
    from ....utils import TestTimes



def test_DriverPhueChange(
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


    assert homie.refresh()


    planets = bodies.planets

    family = 'philips'

    for planet in planets:

        desire = desires[
            f'{planet}_active']

        driver = (
            desire.wheres[1]
            .drivers[0])

        assert isinstance(
            driver, DriverPhueChange)


        attrs = lattrs(driver)

        assert attrs == [
            '_HomieDriver__plugin',
            '_HomieDriver__params']


        assert inrepr(
            'change.DriverPhueChange',
            driver)

        assert isinstance(
            hash(driver), int)

        assert instr(
            'change.DriverPhueChange',
            driver)


        driver.validate()

        assert driver.plugin

        assert driver.family == family

        assert driver.kinds == ['where']

        assert driver.params


        time = times.current

        assert driver.where(time)



def test_DriverPhueChange_cover(
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
        devices:
         jupiter_nexist:
          origin: jupiter_philips
          label: Not exists
         neptune_nexist:
          origin: neptune_philips
          label: Not exists
        desires:
         pytest:
          groups:
          - ganymede
          - halimede
          wheres:
          - philips_change:
             devices:
             - jupiter_button
             - neptune_button
             since: 900
          - philips_change:
             devices:
             - jupiter_nexist
             - neptune_nexist
        """)  # noqa: LIT003

    homie = homie_factory(
        config_factory(tmp_path),
        respx_mock=respx_mock)


    childs = homie.childs

    desire = (
        childs.desires
        ['pytest'])


    assert homie.refresh()


    time = times.current

    wheres = desire.wheres

    for where in wheres:

        (where.drivers[0]
         .where(time))
