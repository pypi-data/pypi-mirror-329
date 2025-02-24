"""
Functions and routines associated with Enasis Network Homie Automate.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from copy import deepcopy
from pathlib import Path

from encommon.types import DictStrAny
from encommon.utils import save_text

from pytest import fixture

from respx import MockRouter

from . import EXAMPLES
from . import PROJECT
from .homie import Homie
from .homie import HomieConfig
from .homie import HomieService
from .hubitat.test import mock_hubi
from .philips.test import mock_phue
from .restful import RestfulService
from .ubiquiti.test import mock_ubiq
from .utils import TestBodies
from .utils import TestTimes



def config_factory(
    tmp_path: Path,
) -> HomieConfig:
    """
    Construct the instance for use in the downstream tests.

    :param tmp_path: pytest object for temporal filesystem.
    :returns: Newly constructed instance of related class.
    """

    content = (
        f"""

        enconfig:
          paths:
            - {EXAMPLES}
            - {tmp_path}/homie

        enlogger:
          stdo_level: info

        encrypts:
          phrases:
            enhomie:
              phrase: oIUc2odGYMKycATXsvXTMzxe0Qbq4z3YPPIWS8fH_uU=

        database: >-
          sqlite:///{tmp_path}/db

        """)

    config_path = (
        tmp_path / 'config.yml')

    save_text(
        config_path, content)

    sargs = {
        'config': config_path,
        'dryrun': False,
        'potent': True,
        'console': True,
        'debug': True,
        'idesire': 1,
        'iupdate': 1,
        'ihealth': 1,
        'atimeout': 1,
        'utimeout': 1,
        'stimeout': 1,
        'paction': True,
        'pupdate': True,
        'pstream': True,
        'paspire': True,
        'pdesire': True}

    return HomieConfig(sargs)



@fixture
def config(
    tmp_path: Path,
) -> HomieConfig:
    """
    Construct the instance for use in the downstream tests.

    :param tmp_path: pytest object for temporal filesystem.
    :returns: Newly constructed instance of related class.
    """

    return config_factory(tmp_path)



@fixture
def times() -> TestTimes:
    """
    Return the simple mapping of what to replace in sample.

    :returns: Simple mapping of what to replace in sample.
    """

    return TestTimes()



@fixture
def bodies() -> TestBodies:
    """
    Return the simple mapping of what to replace in sample.

    :returns: Simple mapping of what to replace in sample.
    """

    return TestBodies()



def replaces_factory() -> DictStrAny:
    """
    Return the complete mapping of what to replace in sample.

    :returns: Complete mapping of what to replace in sample.
    """

    times = TestTimes()

    replaces = {

        '__TIMESTAMP_START__': (
            times.start.simple),

        '__TIMESTAMP_MIDDLE__': (
            times.middle.simple),

        '__TIMESTAMP_FINAL__': (
            times.final.simple),

        '__TIMESTAMP_CRRNT__': (
            times.current.simple),

        '__UNIXEPOCH_START__': (
            times.start.spoch),

        '__UNIXEPOCH_MIDDLE__': (
            times.middle.spoch),

        '__UNIXEPOCH_FINAL__': (
            times.final.spoch),

        '__UNIXEPOCH_CRRNT__': (
            times.current.spoch)}

    return deepcopy(replaces)



@fixture
def replaces(
    tmp_path: Path,
) -> DictStrAny:
    """
    Return the complete mapping of what replaced in sample.

    :param tmp_path: pytest object for temporal filesystem.
    :returns: Complete mapping of what replaced in sample.
    """

    replaces = replaces_factory()

    return replaces | {
        'PROJECT': PROJECT,
        'TMPPATH': tmp_path}



def homie_factory(
    config: HomieConfig,
    respx_mock: MockRouter,
) -> Homie:
    """
    Construct the instance for use in the downstream tests.

    :param config: Primary class instance for configuration.
    :param respx_mock: Object for mocking request operation.
    :returns: Newly constructed instance of related class.
    """

    replaces = replaces_factory()

    mock_hubi(respx_mock, replaces)
    mock_phue(respx_mock, replaces)
    mock_ubiq(respx_mock, replaces)

    return Homie(config)



@fixture
def homie(
    config: HomieConfig,
    respx_mock: MockRouter,
) -> Homie:
    """
    Construct the instance for use in the downstream tests.

    :param config: Primary class instance for configuration.
    :param respx_mock: Object for mocking request operation.
    :returns: Newly constructed instance of related class.
    """

    return homie_factory(
        config, respx_mock)



def service_factory(
    homie: Homie,
    respx_mock: MockRouter,
) -> HomieService:
    """
    Construct the instance for use in the downstream tests.

    :param homie: Primary class instance for Homie Automate.
    :param respx_mock: Object for mocking request operation.
    :returns: Newly constructed instance of related class.
    """

    return HomieService(homie)



@fixture
def service(
    homie: Homie,
    respx_mock: MockRouter,
) -> HomieService:
    """
    Construct the instance for use in the downstream tests.

    :param homie: Primary class instance for Homie Automate.
    :param respx_mock: Object for mocking request operation.
    :returns: Newly constructed instance of related class.
    """

    return service_factory(
        homie, respx_mock)



def restful_factory(
    homie: Homie,
) -> RestfulService:
    """
    Construct the instance for use in the downstream tests.

    :param homie: Primary class instance for Homie Automate.
    :returns: Newly constructed instance of related class.
    """

    return RestfulService(homie)



@fixture
def restful(
    homie: Homie,
) -> RestfulService:
    """
    Construct the instance for use in the downstream tests.

    :param homie: Primary class instance for Homie Automate.
    :returns: Newly constructed instance of related class.
    """

    return restful_factory(homie)
