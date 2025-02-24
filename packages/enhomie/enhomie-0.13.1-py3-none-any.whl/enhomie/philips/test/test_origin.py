"""
Functions and routines associated with Enasis Network Homie Automate.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from json import loads
from typing import TYPE_CHECKING

from encommon.types import DictStrAny
from encommon.types import lattrs
from encommon.utils import load_sample
from encommon.utils import prep_sample
from encommon.utils import read_text
from encommon.utils import rvrt_sample
from encommon.utils.sample import ENPYRWS

from . import SAMPLES
from ..origin import PhueOrigin
from ..update import PhueUpdateItem

if TYPE_CHECKING:
    from ...homie import Homie
    from ...homie import HomieService
    from ...utils import TestBodies



def test_PhueOrigin(
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

    samples = SAMPLES / 'origin'


    planets = bodies.planets

    family = 'philips'

    for planet in planets:

        name = f'{planet}_{family}'

        origin = origins[name]

        assert isinstance(
            origin, PhueOrigin)


        attrs = lattrs(origin)

        assert attrs == [
            '_HomieChild__homie',
            '_HomieChild__name',
            '_HomieChild__params',
            '_PhueOrigin__bridge',
            '_PhueOrigin__fetch',
            '_PhueOrigin__merge']


        origin.validate()

        assert origin.homie

        assert origin.name == name

        assert origin.family == family

        assert origin.kind == 'origin'

        assert origin.params

        assert origin.dumped


        assert origin.bridge

        assert not origin.fetch

        assert not origin.merge


        assert origin.refresh()

        assert origin.fetch

        assert origin.merge


        sample_path = (
            f'{samples}/fetch'
            f'/{planet}.json')

        sample = load_sample(
            path=sample_path,
            update=ENPYRWS,
            content=origin.fetch,
            replace=replaces)

        expect = prep_sample(
            content=origin.fetch,
            replace=replaces)

        assert expect == sample


        sample_path = (
            f'{samples}/merge'
            f'/{planet}.json')

        sample = load_sample(
            path=sample_path,
            update=ENPYRWS,
            content=origin.merge,
            replace=replaces)

        expect = prep_sample(
            content=origin.merge,
            replace=replaces)

        assert expect == sample



def test_PhueOrigin_action(
    homie: 'Homie',
    service: 'HomieService',
    bodies: 'TestBodies',
) -> None:
    """
    Perform various tests associated with relevant routines.

    :param homie: Primary class instance for Homie Automate.
    :param service: Ancilary Homie Automate class instance.
    :param bodies: Locations and groups for use in testing.
    """

    childs = homie.childs
    origins = childs.origins
    devices = childs.devices
    groups = childs.groups
    scenes = childs.scenes

    scene1 = scenes['active']
    scene2 = scenes['standby']


    planets = bodies.planets
    moons = dict(bodies.moons)

    for planet in planets:

        origin = origins[
            f'{planet}_philips']

        assert isinstance(
            origin, PhueOrigin)

        assert origin.refresh()


        moon = moons[planet]

        device = devices[
            f'{planet}_light1']

        group = groups[moon]


        aitem = (
            origin.get_action(
                target=device,
                scene=scene2))

        assert not (
            origin.set_action(
                device, aitem))


        aitem = (
            origin.get_action(
                target=group,
                scene=scene2))

        assert not (
            origin.set_action(
                group, aitem))


        aitem = (
            origin.get_action(
                target=device,
                state='nopower',
                color='ff00cc',
                level=100))

        assert (
            origin.set_action(
                device, aitem))

        assert (
            origin.set_action(
                device, aitem,
                change=False))


        aitem = (
            origin.get_action(
                target=device,
                state='poweron',
                color='003333',
                level=80))

        assert not (
            origin.set_action(
                device, aitem))


        aitem = (
            origin.get_action(
                target=group,
                scene=scene1.name))

        assert (
            origin.set_action(
                group, aitem,
                change=False))



def test_PhueOrigin_update(
    homie: 'Homie',
    service: 'HomieService',
    replaces: DictStrAny,
    bodies: 'TestBodies',
) -> None:
    """
    Perform various tests associated with relevant routines.

    :param homie: Primary class instance for Homie Automate.
    :param service: Ancilary Homie Automate class instance.
    :param replaces: Mapping of what to replace in samples.
    :param bodies: Locations and groups for use in testing.
    """

    assert service.updates

    childs = homie.childs
    origins = childs.origins
    member = service.updates
    uqueue = member.uqueue

    samples = SAMPLES / 'stream'


    planets = bodies.planets

    for planet in planets:

        origin = origins[
            f'{planet}_philips']

        assert isinstance(
            origin, PhueOrigin)

        assert origin.refresh()

        fetch = origin.fetch


        uitem = origin.get_update()

        assert isinstance(
            uitem, PhueUpdateItem)

        uitem.fetch['foo'] = 'bar'

        origin.set_update(uitem)

        origin.put_update(uqueue)

        _fetch = origin.fetch


        assert _fetch != fetch


        source = read_text(
            f'{samples}/dumped'
            f'/{planet}.json')

        source = rvrt_sample(
            sample=source,
            replace=replaces)

        sample = loads(source)

        sitem = (
            origin.get_stream(
                sample[3]['event']))

        origin.set_update(sitem)

        fetch = origin.fetch


        assert _fetch != fetch


    assert uqueue.qsize == 2



def test_PhueOrigin_stream(
    homie: 'Homie',
    service: 'HomieService',
    bodies: 'TestBodies',
) -> None:
    """
    Perform various tests associated with relevant routines.

    :param homie: Primary class instance for Homie Automate.
    :param service: Ancilary Homie Automate class instance.
    :param bodies: Locations and groups for use in testing.
    """

    assert service.streams

    childs = homie.childs
    origins = childs.origins
    member = service.streams
    squeue = member.squeue


    planets = bodies.planets

    event = {'foo': 'bar'}

    for planet in planets:

        origin = origins[
            f'{planet}_philips']

        assert isinstance(
            origin, PhueOrigin)

        origin.put_stream(
            squeue, event)


    assert squeue.qsize == 2



def test_PhueOrigin_source(
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


    planets = bodies.planets
    moons = dict(bodies.moons)

    for planet in planets:

        origin = origins[
            f'{planet}_philips']

        origin.refresh()


        source = origin.source(
            label='Nothing')

        assert source is None


        moon = moons[planet]

        source = origin.source(
            kind='scene',
            label='active',
            relate=groups[moon])

        assert source is not None


        source = origin.source(
            kind='group',
            label=planet)

        assert source is not None

        source = origin.source(
            kind='group',
            label=moon)

        assert source is not None
