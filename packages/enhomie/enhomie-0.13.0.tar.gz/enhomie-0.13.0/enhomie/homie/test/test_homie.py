"""
Functions and routines associated with Enasis Network Homie Automate.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from typing import TYPE_CHECKING

from encommon.types import DictStrAny
from encommon.types import inrepr
from encommon.types import instr
from encommon.types import lattrs
from encommon.utils import load_sample
from encommon.utils import prep_sample
from encommon.utils.sample import ENPYRWS

from . import SAMPLES
from ..config import HomieConfig
from ..homie import Homie
from ..threads import HomieThreadItem

if TYPE_CHECKING:
    from ...utils import TestBodies



def test_Homie(
    homie: Homie,
    replaces: DictStrAny,
) -> None:
    """
    Perform various tests associated with relevant routines.

    :param homie: Primary class instance for Homie Automate.
    :param replaces: Mapping of what to replace in samples.
    """


    attrs = lattrs(homie)

    assert attrs == [
        '_Homie__config',
        '_Homie__logger',
        '_Homie__jinja2',
        '_Homie__persist',
        '_Homie__childs',
        '_Homie__desired',
        '_Homie__aspired']


    assert inrepr(
        'homie.Homie',
        homie)

    assert isinstance(
        hash(homie), int)

    assert instr(
        'homie.Homie',
        homie)


    assert homie.config

    assert homie.logger

    assert homie.jinja2

    assert homie.persist

    assert homie.childs

    assert homie.params

    assert not homie.dryrun

    assert homie.potent

    assert homie.desired

    assert homie.aspired


    assert homie.refresh()


    sample_path = (
        SAMPLES / 'dumped.json')

    sample = load_sample(
        path=sample_path,
        update=ENPYRWS,
        content=homie.dumped,
        replace=replaces)

    expect = prep_sample(
        content=homie.dumped,
        replace=replaces)

    assert expect == sample



def test_Homie_printer(
    homie: Homie,
) -> None:
    """
    Perform various tests associated with relevant routines.

    :param homie: Primary class instance for Homie Automate.
    """

    childs = homie.childs
    origins = childs.origins

    origin = origins[
        'jupiter_philips']

    model = HomieThreadItem

    item = model(origin)

    homie.printer(item)



def test_Homie_actions(
    homie: Homie,
    bodies: 'TestBodies',
) -> None:
    """
    Perform various tests associated with relevant routines.

    :param homie: Primary class instance for Homie Automate.
    :param bodies: Locations and groups for use in testing.
    """

    childs = homie.childs
    devices = childs.devices
    groups = childs.groups


    assert homie.refresh()


    moons = (
        dict(bodies.moons)
        .items())

    for planet, moon in moons:


        device = devices[
            f'{planet}_light2']

        aitems = (
            homie.get_actions(
                target=device,
                state='poweron',
                color='ff00cc',
                level=69))

        assert len(aitems) == 1

        assert homie.set_actions(
            aitems, force=True)

        assert homie.set_actions(
            aitems, change=False)


        device = devices[
            f'{planet}_light1']

        aitems = (
            homie.get_actions(
                target=device,
                state='nopower',
                color='ff00cc',
                level=100))

        assert len(aitems) == 1

        assert homie.set_actions(
            aitems, force=True)

        assert homie.set_actions(
            aitems, change=False)


        group = groups[moon]

        aitems = (
            homie.get_actions(
                target=group,
                state='poweron',
                color='ff00cc',
                level=69))

        assert len(aitems) == 2

        assert homie.set_actions(
            aitems, force=True)

        assert homie.set_actions(
            aitems, change=False)


        aitems = (
            homie
            .get_actions(group))

        assert len(aitems) == 0



def test_Homie_jinja2(
    homie: Homie,
    replaces: DictStrAny,
) -> None:
    """
    Perform various tests associated with relevant routines.

    :param homie: Primary class instance for Homie Automate.
    :param replaces: Mapping of what to replace in samples.
    """

    parsed = homie.j2parse(
        '{{ foo }}',
        {'foo': 'bar'})

    assert parsed == 'bar'



def test_Homie_cover(
) -> None:
    """
    Perform various tests associated with relevant routines.
    """

    Homie(HomieConfig())
