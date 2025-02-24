"""
Functions and routines associated with Enasis Network Homie Automate.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from dataclasses import dataclass
from typing import Literal
from typing import get_args

from encommon.times import Time



STARTED = Time('now')



Planets = Literal[
    'jupiter', 'neptune']

PLANETS = set(
    get_args(Planets))

_PLANETS = tuple[Planets, ...]



Moons = Literal[
    'ganymede', 'halimede']

MOONS = set(
    get_args(Moons))

MoonPair = tuple[
    Planets, Moons]

_MOONS = tuple[MoonPair, ...]



@dataclass(frozen=True)
class TestTimes:
    """
    Contain the times used within various tests in project.
    """

    start: Time = STARTED.shift('-1w@h')
    middle: Time = STARTED.shift('-1d@h')
    final: Time = STARTED.shift('-1h@h')
    current: Time = STARTED.shift('-1m')



@dataclass(frozen=True)
class TestBodies:
    """
    Contain the planets used to reference test sample sets.
    """

    planets: _PLANETS = tuple(PLANETS)

    moons: _MOONS = (
        ('jupiter', 'ganymede'),
        ('neptune', 'halimede'))
