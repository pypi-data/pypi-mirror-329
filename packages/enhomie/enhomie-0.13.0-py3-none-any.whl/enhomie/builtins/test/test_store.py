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

from ..store import DriverBltnStore
from ...conftest import config_factory
from ...conftest import homie_factory

if TYPE_CHECKING:
    from ...homie import Homie
    from ...utils import TestBodies
    from ...utils import TestTimes



def test_DriverBltnStore(
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

    family = 'builtins'

    for planet in planets:

        desire = desires[
            f'{planet}_active']

        driver = (
            desire.wheres[2]
            .drivers[0])

        assert isinstance(
            driver, DriverBltnStore)


        attrs = lattrs(driver)

        assert attrs == [
            '_HomieDriver__plugin',
            '_HomieDriver__params']


        assert inrepr(
            'store.DriverBltnStore',
            driver)

        assert isinstance(
            hash(driver), int)

        assert instr(
            'store.DriverBltnStore',
            driver)


        driver.validate()

        assert driver.plugin

        assert driver.family == family

        assert driver.kinds == ['where']

        assert driver.params


        time = times.current

        assert driver.where(time)



def test_DriverBltnStore_cover(
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
          groups:
          - ganymede
          - halimede
          wheres:
          - builtins_store:
             unique: test1
             operator: absent
          - builtins_store:
             unique: test2
             operator: present
          - builtins_store:
             unique: test3
             operator: neq
             value: value1
          - builtins_store:
             unique: test3
             operator: eq
             value: value3
          - builtins_store:
             unique: test4
             operator: lte
             value: 400000
          - builtins_store:
             unique: test4
             operator: lt
             value: 500000
          - builtins_store:
             unique: test5
             operator: gte
             value: 500000
          - builtins_store:
             unique: test5
             operator: gt
             value: 400000
        """)  # noqa: LIT003

    homie = homie_factory(
        config_factory(tmp_path),
        respx_mock=respx_mock)


    childs = homie.childs

    desire = (
        childs.desires
        ['pytest'])


    homie.persist.insert(
        'test2', 'value2')

    homie.persist.insert(
        'test3', 'value3')

    homie.persist.insert(
        'test4', 400000)

    homie.persist.insert(
        'test5', 500000)


    time = times.current

    wheres = desire.wheres

    for where in wheres:

        (where.drivers[0]
         .where(time))
