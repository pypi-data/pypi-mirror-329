"""
Functions and routines associated with Enasis Network Homie Automate.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from dataclasses import asdict
from typing import TYPE_CHECKING

from encommon.types import DictStrAny
from encommon.utils import load_sample
from encommon.utils import prep_sample
from encommon.utils.sample import ENPYRWS

from . import SAMPLES
from ..stream import PhueStreamItem

if TYPE_CHECKING:
    from ...homie import HomieService
    from ...utils import TestBodies



def test_PhueStreamItem(
    service: 'HomieService',
    bodies: 'TestBodies',
) -> None:
    """
    Perform various tests associated with relevant routines.

    :param service: Ancilary Homie Automate class instance.
    :param bodies: Locations and groups for use in testing.
    """

    homie = service.homie
    childs = homie.childs
    origins = childs.origins

    model = PhueStreamItem


    planets = bodies.planets

    event = {'foo': 'bar'}

    for planet in planets:

        name = f'{planet}_philips'

        origin = origins[name]


        item = model(
            origin, event)


        assert item.origin == name

        assert item.event == event



def test_PhueStream_samples(
    service: 'HomieService',
    replaces: DictStrAny,
    bodies: 'TestBodies',
) -> None:
    """
    Perform various tests associated with relevant routines.

    :param service: Ancilary Homie Automate class instance.
    :param replaces: Mapping of what to replace in samples.
    :param bodies: Locations and groups for use in testing.
    """

    assert service.streams

    member = service.streams
    threads = member.threads
    squeue = member.squeue
    cancel = member.cancel

    samples = SAMPLES / 'stream'


    planets = bodies.planets

    for planet in planets:

        cancel.clear()

        thread = threads[
            f'{planet}_philips']

        thread.operate()

        assert squeue.qsize == 8

        cancel.set()

        thread.operate()

        assert squeue.qsize == 8


        output: list[DictStrAny] = []

        while not squeue.empty:

            sitem = squeue.get()

            append = asdict(sitem)

            del append['time']

            output.append(append)


        sample_path = (
            f'{samples}/dumped'
            f'/{planet}.json')

        sample = load_sample(
            path=sample_path,
            update=ENPYRWS,
            content=output,
            replace=replaces)

        expect = prep_sample(
            content=output,
            replace=replaces)

        assert expect == sample
