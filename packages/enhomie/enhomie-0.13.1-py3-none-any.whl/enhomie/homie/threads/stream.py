"""
Functions and routines associated with Enasis Network Homie Automate.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from copy import deepcopy
from dataclasses import dataclass
from typing import TYPE_CHECKING

from encommon.types import DictStrAny

from .thread import HomieThread
from .thread import HomieThreadItem

if TYPE_CHECKING:
    from ..childs import HomieOrigin



@dataclass
class HomieStreamItem(HomieThreadItem):
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

        event = deepcopy(event)

        self.event = event

        super().__init__(origin)



class HomieStream(HomieThread):
    """
    Common methods and routines for Homie Automate threads.
    """


    def operate(
        self,
    ) -> None:
        """
        Perform the operation related to Homie service threads.
        """

        member = self.member
        vacate = member.vacate

        if vacate.is_set():
            return None

        self.operate_streams()


    def operate_streams(
        self,
    ) -> None:
        """
        Perform the operation related to Homie service threads.
        """

        raise NotImplementedError
