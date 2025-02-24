"""
Functions and routines associated with Enasis Network Homie Automate.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from dataclasses import dataclass
from time import sleep as block_sleep
from typing import TYPE_CHECKING

from encommon.types import DictStrAny

from httpx import ReadTimeout

from .origin import PhueOrigin
from ..homie.threads import HomieStream
from ..homie.threads import HomieStreamItem

if TYPE_CHECKING:
    from ..homie.childs import HomieOrigin



@dataclass
class PhueStreamItem(HomieStreamItem):
    """
    Contain information for sharing using the Python queue.
    """

    event: DictStrAny


    def __init__(
        self,
        origin: 'HomieOrigin',
        event: DictStrAny,
    ) -> None:
        """
        Initialize instance for class using provided parameters.
        """

        super().__init__(
            origin, event)



class PhueStream(HomieStream):
    """
    Common methods and routines for Homie Automate threads.
    """


    def operate_streams(
        self,
    ) -> None:
        """
        Perform the operation related to Homie service threads.
        """

        homie = self.homie
        member = self.member
        origin = self.origin

        assert isinstance(
            origin, PhueOrigin)

        params = homie.params
        squeue = member.squeue
        cancel = member.cancel

        request = (
            origin.bridge
            .events_block)

        timeout = (
            params.service
            .timeout.stream)

        stream = request(
            timeout=timeout)

        try:

            homie.logger.log_i(
                base=self,
                name=origin,
                status='reading')

            for event in stream:

                if cancel.is_set():
                    break

                origin.put_stream(
                    squeue, event)

            homie.logger.log_i(
                base=self,
                name=origin,
                status='closed')

        except ReadTimeout:

            homie.logger.log_i(
                base=self,
                name=origin,
                status='timeout')

        except Exception as reason:

            homie.logger.log_e(
                base=self,
                name=origin,
                status='exception',
                exc_info=reason)

            block_sleep(1)
