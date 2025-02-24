"""
Functions and routines associated with Enasis Network Homie Automate.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from typing import TYPE_CHECKING

from encommon.types import DictStrAny
from encommon.types import lattrs
from encommon.utils import load_sample
from encommon.utils import prep_sample
from encommon.utils.sample import ENPYRWS

from . import SAMPLES
from ..origin import HubiOrigin
from ..update import HubiUpdateItem

if TYPE_CHECKING:
    from ...homie import Homie
    from ...homie import HomieService
    from ...utils import TestBodies



def test_HubiOrigin(
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

    family = 'hubitat'

    for planet in planets:

        name = f'{planet}_{family}'

        origin = origins[name]

        assert isinstance(
            origin, HubiOrigin)


        attrs = lattrs(origin)

        assert attrs == [
            '_HomieChild__homie',
            '_HomieChild__name',
            '_HomieChild__params',
            '_HubiOrigin__bridge',
            '_HubiOrigin__fetch',
            '_HubiOrigin__merge']


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



def test_HubiOrigin_action(
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
    scenes = childs.scenes

    scene1 = scenes['active']
    scene2 = scenes['standby']


    planets = bodies.planets

    for planet in planets:

        origin = origins[
            f'{planet}_hubitat']

        assert isinstance(
            origin, HubiOrigin)

        assert origin.refresh()


        device = devices[
            f'{planet}_light2']


        aitem = (
            origin.get_action(
                target=device,
                scene=scene2))

        assert not (
            origin.set_action(
                device, aitem))


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
                level=20))

        assert not (
            origin.set_action(
                device, aitem))


        aitem = (
            origin.get_action(
                target=device,
                scene=scene1.name))

        assert (
            origin.set_action(
                device, aitem,
                change=False))



def test_HubiOrigin_update(
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

    assert service.updates

    childs = homie.childs
    origins = childs.origins
    member = service.updates
    uqueue = member.uqueue


    planets = bodies.planets

    for planet in planets:

        origin = origins[
            f'{planet}_hubitat']

        assert isinstance(
            origin, HubiOrigin)

        assert origin.refresh()

        fetch = origin.fetch


        uitem = origin.get_update()

        assert isinstance(
            uitem, HubiUpdateItem)

        uitem.fetch[0]['foo'] = 'bar'

        origin.set_update(uitem)

        origin.put_update(uqueue)

        _fetch = origin.fetch


        assert _fetch != fetch


    assert uqueue.qsize == 2



def test_HubiOrigin_source(
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


    planets = bodies.planets

    for planet in planets:

        origin = origins[
            f'{planet}_hubitat']


        origin.refresh()


        source = origin.source(
            label='Nothing')

        assert source is None


        source = origin.source(
            label=f'{planet} Light')

        assert source is not None


        source = origin.source(
            kind='device',
            unique='1')

        assert source is not None
