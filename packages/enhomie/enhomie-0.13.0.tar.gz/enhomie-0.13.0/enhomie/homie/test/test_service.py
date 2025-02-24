"""
Functions and routines associated with Enasis Network Homie Automate.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from pathlib import Path
from threading import Thread
from time import sleep as block_sleep
from typing import TYPE_CHECKING

from encommon.types import inrepr
from encommon.types import instr
from encommon.types import lattrs
from encommon.utils import save_text

from respx import MockRouter

from ..threads import HomieUpdateItem
from ...conftest import config_factory
from ...conftest import homie_factory
from ...conftest import service_factory

if TYPE_CHECKING:
    from ..service import HomieService



def test_HomieService(
    service: 'HomieService',
) -> None:
    """
    Perform various tests associated with relevant routines.

    :param service: Ancilary Homie Automate class instance.
    """


    attrs = lattrs(service)

    assert attrs == [
        '_HomieService__homie',
        '_HomieService__actions',
        '_HomieService__updates',
        '_HomieService__streams',
        '_HomieService__restful',
        '_HomieService__timer',
        '_HomieService__vacate',
        '_HomieService__cancel',
        '_HomieService__started']


    assert inrepr(
        'service.HomieService',
        service)

    assert isinstance(
        hash(service), int)

    assert instr(
        'service.HomieService',
        service)


    assert service.homie

    assert service.params

    assert service.actions

    assert service.updates

    assert service.streams

    assert not service.restful

    assert len(service.running) == 0

    assert len(service.zombies) == 12


    service.start()


    thread = Thread(
        target=service.operate)

    thread.start()


    block_sleep(10)

    assert service.running

    assert not service.zombies

    assert service.congest

    service.soft()

    while service.enqueue:
        block_sleep(1)  # NOCVR

    while service.running:
        block_sleep(1)  # NOCVR

    service.stop()

    thread.join()

    assert service.zombies

    assert not service.congest

    assert not service.enqueue



def test_HomieService_dryrun(
    service: 'HomieService',
) -> None:
    """
    Perform various tests associated with relevant routines.

    :param service: Ancilary Homie Automate class instance.
    """

    homie = service.homie
    params = homie.params

    params.dryrun = True


    service.start()


    thread = Thread(
        target=service.operate)

    thread.start()


    block_sleep(10)

    assert service.running

    assert not service.zombies

    assert service.congest

    service.soft()

    while service.enqueue:
        block_sleep(1)  # NOCVR

    while service.running:
        block_sleep(1)  # NOCVR

    service.stop()

    thread.join()

    assert service.zombies

    assert not service.congest

    assert not service.enqueue


    block_sleep(1.1)

    service.operate_healths()



def test_HomieService_healths(
    service: 'HomieService',
) -> None:
    """
    Perform various tests associated with relevant routines.

    :param service: Ancilary Homie Automate class instance.
    """

    assert service.updates

    homie = service.homie
    childs = homie.childs
    origins = childs.origins
    member = service.updates
    threads = member.threads

    origin = origins[
        'jupiter_philips']

    thread = threads[
        'jupiter_philips']

    uqueue = thread.uqueue

    model = HomieUpdateItem

    item = model(origin)


    for _ in range(6):
        uqueue.put(item)


    assert service.congest

    service.operate_healths()



def test_HomieService_cover(
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
        service:
         members:
          actions: false
          updates: false
          streams: false
        """)  # noqa: LIT003

    homie = homie_factory(
        config_factory(tmp_path),
        respx_mock=respx_mock)

    service = service_factory(
        homie, respx_mock)


    service.stop()
    service.soft()
    service.start()
    service.start()
    service.soft()
    service.soft()
    service.stop()
    service.stop()

    service.operate_updates()
    service.operate_streams()


    assert not service.actions

    assert not service.updates

    assert not service.streams
