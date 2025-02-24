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

from fastapi.testclient import TestClient

from respx import MockRouter

from ...conftest import config_factory
from ...conftest import homie_factory
from ...conftest import restful_factory



def test_RestfulService(
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
         bind_port: 8421
        """)  # noqa: LIT003

    homie = homie_factory(
        config_factory(tmp_path),
        respx_mock=respx_mock)


    restful = (
        restful_factory(homie))


    attrs = lattrs(restful)

    assert attrs == [
        '_RestfulService__homie',
        '_RestfulService__fastapi',
        '_RestfulService__uvicorn',
        '_RestfulService__thread',
        '_RestfulService__stopped',
        '_RestfulService__started']


    assert inrepr(
        'service.RestfulService',
        restful)

    assert isinstance(
        hash(restful), int)

    assert instr(
        'service.RestfulService',
        restful)


    assert restful.homie

    assert restful.params

    assert restful.fastapi

    assert not restful.running


    restful.start()


    thread = Thread(
        target=restful.operate)

    thread.start()


    block_sleep(5)

    assert restful.running

    restful.stop()

    while restful.running:
        block_sleep(1)  # NOCVR

    thread.join()

    assert not restful.running



def test_RestfulService_forbid(
    client: TestClient,
    mismatch: TestClient,
    invalid: TestClient,
) -> None:
    """
    Perform various tests associated with relevant routines.

    :param client: Used when testing the FastAPI endpoints.
    :param mismatch: Used when testing the FastAPI endpoints.
    :param invalid: Used when testing the FastAPI endpoints.
    """

    path = '/api/persists'


    response = client.get(path)

    assert response.status_code == 200


    response = mismatch.get(path)

    assert response.status_code == 401


    response = invalid.get(path)

    assert response.status_code == 401



def test_RestfulService_cover(
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
         bind_port: 8422
        """)  # noqa: LIT003

    homie = homie_factory(
        config_factory(tmp_path),
        respx_mock=respx_mock)

    restful = (
        restful_factory(homie))


    restful.stop()
    restful.start()
    restful.start()
    restful.stop()
    restful.stop()
