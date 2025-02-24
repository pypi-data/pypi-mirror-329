"""
Functions and routines associated with Enasis Network Homie Automate.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from dataclasses import dataclass
from typing import Any
from typing import TYPE_CHECKING
from typing import Union

from encommon.times import Timer
from encommon.types import NCNone

from .thread import HomieThread
from .thread import HomieThreadItem

if TYPE_CHECKING:
    from .stream import HomieStreamItem
    from ..childs import HomieOrigin



HomieUpdateBase = Union[
    'HomieUpdateItem',
    'HomieStreamItem']

_UPDATES = set['HomieOrigin']



@dataclass
class HomieUpdateItem(HomieThreadItem):
    """
    Contain information for sharing using the Python queue.
    """


    def __init__(
        self,
        origin: 'HomieOrigin',
    ) -> None:
        """
        Initialize instance for class using provided parameters.
        """

        super().__init__(origin)



class HomieUpdate(HomieThread):
    """
    Common methods and routines for Homie Automate threads.
    """

    __timer: Timer


    def __init__(
        self,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        """
        Initialize instance for class using provided parameters.
        """

        super().__init__(
            *args, **kwargs)


        homie = self.homie
        params = homie.params

        respite = (
            params.service
            .respite)

        timer = Timer(
            respite.update,
            start='min')

        self.__timer = timer


    def operate(
        self,
    ) -> None:
        """
        Perform the operation related to Homie service threads.
        """

        member = self.member
        timer = self.__timer
        vacate = member.vacate

        if timer.pause():
            return None

        if vacate.is_set():
            return None

        homie = self.homie
        params = homie.params
        origin = self.origin

        timeout = (
            params.service
            .timeout.update)

        refresh = (
            origin
            .refresh(timeout))

        if refresh is False:
            return NCNone

        origin.put_update(
            member.uqueue)


    def operate_updates(
        self,
    ) -> None:
        """
        Perform the operation related to Homie service threads.
        """

        member = self.member
        homie = member.homie
        childs = homie.childs
        vacate = member.vacate
        uqueue = member.uqueue
        squeue = self.squeue

        origins = (
            childs.origins
            .values())


        updates: _UPDATES = set()


        def _set_update() -> None:

            name = sitem.origin
            _name = origin.name

            if name != _name:
                return None

            result = (
                origin
                .set_update(sitem))

            if result is False:
                return NCNone

            updates.add(origin)


        while not squeue.empty:

            sitem = squeue.get()

            if vacate.is_set():
                continue

            if self.expired(sitem):
                continue

            for origin in origins:
                _set_update()


        for origin in updates:

            (origin
             .put_update(uqueue))


        super().operate_updates()
