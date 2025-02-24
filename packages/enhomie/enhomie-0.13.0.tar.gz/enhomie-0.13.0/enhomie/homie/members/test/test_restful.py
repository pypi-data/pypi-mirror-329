"""
Functions and routines associated with Enasis Network Homie Automate.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from pathlib import Path
from threading import Thread
from time import sleep as block_sleep

from encommon.types import inrepr
from encommon.types import instr
from encommon.types import lattrs
from encommon.utils import save_text

from respx import MockRouter

from ....conftest import config_factory
from ....conftest import homie_factory
from ....conftest import service_factory
from ....restful.conftest import _create_client



def test_HomieRestful(  # noqa: CFQ001
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
        restful:
         bind_port: 8423
        service:
         members:
          actions: false
          updates: false
          streams: false
          restful: true
        """)  # noqa: LIT003

    homie = homie_factory(
        config_factory(tmp_path),
        respx_mock=respx_mock)

    service = service_factory(
        homie, respx_mock)


    assert service.restful

    member = service.restful


    attrs = lattrs(member)

    assert attrs == [
        '_HomieMember__homie',
        '_HomieMember__threads',
        '_HomieMember__aqueue',
        '_HomieMember__uqueue',
        '_HomieMember__squeue',
        '_HomieMember__vacate',
        '_HomieMember__cancel',
        '_HomieRestful__restful',
        '_HomieRestful__thread']


    assert inrepr(
        'restful.HomieRestful',
        member)

    assert isinstance(
        hash(member), int)

    assert instr(
        'restful.HomieRestful',
        member)


    assert member.homie

    assert len(member.threads) == 0

    assert member.aqueue

    assert member.uqueue

    assert member.squeue

    assert member.vacate

    assert member.cancel

    assert len(member.running) == 1

    assert member.restful


    member.operate()


    service.start()


    thread = Thread(
        target=service.operate)

    thread.start()


    block_sleep(10)


    status_code = (
        (_create_client(
            member.restful,
            'username:password'))
        .get('/api/docs')
        .status_code)

    assert status_code == 200


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
