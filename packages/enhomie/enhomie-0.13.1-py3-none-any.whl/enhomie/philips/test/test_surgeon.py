"""
Functions and routines associated with Enasis Network Homie Automate.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from json import loads
from typing import TYPE_CHECKING

from encommon.types import DictStrAny
from encommon.utils import load_sample
from encommon.utils import prep_sample
from encommon.utils import read_text
from encommon.utils import rvrt_sample
from encommon.utils.sample import ENPYRWS

from . import SAMPLES
from ..origin import PhueOrigin
from ..surgeon import surgeon

if TYPE_CHECKING:
    from ...homie import Homie
    from ...utils import TestBodies



def test_surgeon(
    homie: 'Homie',
    replaces: DictStrAny,
    bodies: 'TestBodies',
) -> None:
    """
    Perform various tests associated with relevant routines.

    :param homie: Primary class instance for Homie Automate.
    :param replaces: Mapping of what to replace in samples.
    :param bodies: Locations and groups for use in testing.
    """

    childs = homie.childs
    origins = childs.origins

    samples = SAMPLES / 'stream'


    planets = bodies.planets

    for planet in planets:

        origin = origins[
            f'{planet}_philips']

        assert isinstance(
            origin, PhueOrigin)

        assert origin.refresh()

        assert origin.fetch

        fetch = origin.fetch


        source = read_text(
            f'{samples}/dumped'
            f'/{planet}.json')

        source = rvrt_sample(
            sample=source,
            replace=replaces)

        sample = loads(source)


        for loaded in sample:

            event = loaded['event']

            assert surgeon(
                fetch, event)


        sample_path = (
            f'{SAMPLES}/surgeon'
            f'/{planet}.json')

        sample = load_sample(
            path=sample_path,
            update=ENPYRWS,
            content=fetch,
            replace=replaces)

        expect = prep_sample(
            content=fetch,
            replace=replaces)

        assert expect == sample
