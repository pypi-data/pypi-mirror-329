"""
Functions and routines associated with Enasis Network Homie Automate.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from pathlib import Path
from typing import TYPE_CHECKING

from encommon.times import Time
from encommon.types import inrepr
from encommon.types import instr
from encommon.types import lattrs
from encommon.utils import save_text

from respx import MockRouter

from ..period import DriverBltnPeriod
from ...conftest import config_factory
from ...conftest import homie_factory

if TYPE_CHECKING:
    from ...homie import Homie
    from ...utils import TestBodies



def test_DriverBltnPeriod(
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

    family = 'builtins'

    for planet in planets:

        desire = desires[
            f'{planet}_active']

        driver = (
            desire.wheres[3]
            .drivers[0])

        assert isinstance(
            driver, DriverBltnPeriod)


        attrs = lattrs(driver)

        assert attrs == [
            '_HomieDriver__plugin',
            '_HomieDriver__params']


        assert inrepr(
            'period.DriverBltnPeriod',
            driver)

        assert isinstance(
            hash(driver), int)

        assert instr(
            'period.DriverBltnPeriod',
            driver)


        driver.validate()

        assert driver.plugin

        assert driver.family == family

        assert driver.kinds == ['where']

        assert driver.params


        time = Time(
            '05:00',
            tzname='US/Central')

        assert driver.where(time)



def test_DriverBltnPeriod_cover(  # noqa: CFQ001
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
        desires:
         pytest:
          groups:
          - ganymede
          - halimede
          wheres:
          - builtins_period:
             start: '00:00'
             stop: '12:00'
          - builtins_period:
             start: '12:00'
          - builtins_period:
             days: Monday
             start: '00:00'
          - builtins_period:
             start: '12:00'
             stop: '17:00'
          - builtins_period:
             start: '00:00'
             stop: '07:00'
          - builtins_period:
             start: '19:00'
        """)  # noqa: LIT003

    homie = homie_factory(
        config_factory(tmp_path),
        respx_mock=respx_mock)


    childs = homie.childs

    desire = (
        childs.desires
        ['pytest'])


    driver = (
        desire.wheres[0]
        .drivers[0])

    asserts = [
        (Time('00:00'), True),
        (Time('11:00'), True),
        (Time('13:00'), False),
        (Time('23:00'), False)]

    assert all(
        driver.where(x) is y
        for x, y in asserts)


    driver = (
        desire.wheres[1]
        .drivers[0])

    asserts = [
        (Time('00:00'), False),
        (Time('11:00'), False),
        (Time('13:00'), True),
        (Time('23:00'), True)]

    assert all(
        driver.where(x) is y
        for x, y in asserts)


    driver = (
        desire.wheres[2]
        .drivers[0])

    assert driver.where(
        Time('Monday 12:00'))

    assert not driver.where(
        Time('Friday 12:00'))


    driver = (
        desire.wheres[3]
        .drivers[0])

    asserts = [
        (Time('11:30'), False),
        (Time('14:00'), True),
        (Time('18:30'), False)]

    assert all(
        driver.where(x) is y
        for x, y in asserts)


    driver = (
        desire.wheres[4]
        .drivers[0])

    asserts = [
        (Time('00:30'), True),
        (Time('07:30'), False),
        (Time('23:30'), False)]

    assert all(
        driver.where(x) is y
        for x, y in asserts)


    driver = (
        desire.wheres[5]
        .drivers[0])

    asserts = [
        (Time('21:00'), True),
        (Time('02:00'), False)]

    assert all(
        driver.where(x) is y
        for x, y in asserts)
