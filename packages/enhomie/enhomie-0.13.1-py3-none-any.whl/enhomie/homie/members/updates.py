"""
Functions and routines associated with Enasis Network Homie Automate.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from typing import Optional
from typing import TYPE_CHECKING
from typing import Type

from encommon.types import NCNone

from .member import HomieMember
from ...hubitat import HubiUpdate
from ...philips import PhueUpdate
from ...ubiquiti import UbiqUpdate

if TYPE_CHECKING:
    from ..childs import HomieOrigin
    from ..threads import HomieThread



class HomieUpdates(HomieMember):
    """
    Common methods and routines for Homie Automate members.
    """


    def operate(
        self,
    ) -> None:
        """
        Perform the operation related to Homie service members.
        """

        self.operate_streams()


    def operate_streams(
        self,
    ) -> None:
        """
        Perform the operation related to Homie service members.
        """

        vacate = self.vacate
        squeue = self.squeue

        threads = (
            self.threads
            .values())


        def _put_update() -> None:

            name = sitem.origin
            origin = thread.origin
            _name = origin.name

            if name != _name:
                return None

            (thread
             .squeue.put(sitem))


        while not squeue.empty:

            sitem = squeue.get()

            if vacate.is_set():
                continue

            for thread in threads:
                _put_update()


    def get_thread(  # noqa: CFQ004
        self,
        origin: 'HomieOrigin',
    ) -> Optional[Type['HomieThread']]:
        """
        Return the Homie class definition for its instantiation.

        :param origin: Child class instance for Homie Automate.
        :returns: Homie class definition for its instantiation.
        """

        family = origin.family

        if family == 'hubitat':
            return HubiUpdate

        if family == 'philips':
            return PhueUpdate

        if family == 'ubiquiti':
            return UbiqUpdate

        return NCNone
