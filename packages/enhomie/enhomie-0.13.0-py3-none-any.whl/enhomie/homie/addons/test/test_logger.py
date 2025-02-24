"""
Functions and routines associated with Enasis Network Homie Automate.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from threading import Thread
from typing import TYPE_CHECKING

from _pytest.logging import LogCaptureFixture

from encommon.types import inrepr
from encommon.types import instr
from encommon.types import lattrs

if TYPE_CHECKING:
    from ...homie import Homie



def test_HomieLogger(
    homie: 'Homie',
) -> None:
    """
    Perform various tests associated with relevant routines.

    :param homie: Primary class instance for Homie Automate.
    """

    logger = homie.logger


    attrs = lattrs(logger)

    assert attrs == [
        '_HomieLogger__homie']


    assert inrepr(
        'logger.HomieLogger',
        logger)

    assert isinstance(
        hash(logger), int)

    assert instr(
        'logger.HomieLogger',
        logger)



def test_HomieLogger_message(
    homie: 'Homie',
    caplog: LogCaptureFixture,
) -> None:
    """
    Perform various tests associated with relevant routines.

    :param homie: Primary class instance for Homie Automate.
    :param caplog: pytest object for capturing log message.
    """

    logger = homie.logger


    logger.start()

    logger.log_d(about='pytest')
    logger.log_c(about='pytest')
    logger.log_e(about='pytest')
    logger.log_i(about='pytest')
    logger.log_w(about='pytest')

    logger.log(
        level='debug',
        about='pytest')

    logger.stop()

    output = caplog.record_tuples

    assert len(output) == 6

    logger.log_d(about='pytest')
    logger.log_c(about='pytest')
    logger.log_e(about='pytest')
    logger.log_i(about='pytest')
    logger.log_w(about='pytest')

    output = caplog.record_tuples

    assert len(output) == 6



def test_HomieLogger_cover(
    homie: 'Homie',
    caplog: LogCaptureFixture,
) -> None:
    """
    Perform various tests associated with relevant routines.

    :param homie: Primary class instance for Homie Automate.
    :param caplog: pytest object for capturing log message.
    """

    logger = homie.logger
    childs = homie.childs
    devices = childs.devices


    thread = Thread(name='foo')

    device = devices[
        'jupiter_light1']


    logger.log_i(base=thread)
    logger.log_i(item=thread)
    logger.log_i(base=homie)
    logger.log_i(item=homie)
    logger.log_i(name=device)
