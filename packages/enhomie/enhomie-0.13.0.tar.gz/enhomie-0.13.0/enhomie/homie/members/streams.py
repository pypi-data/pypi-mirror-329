"""
Functions and routines associated with Enasis Network Homie Automate.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from typing import Optional
from typing import TYPE_CHECKING
from typing import Type

from .member import HomieMember
from ...philips import PhueStream

if TYPE_CHECKING:
    from ..childs import HomieOrigin
    from ..threads import HomieThread



class HomieStreams(HomieMember):
    """
    Common methods and routines for Homie Automate members.
    """


    def operate(
        self,
    ) -> None:
        """
        Perform the operation related to Homie service members.
        """

        # Nothing to do for member


    def get_thread(
        self,
        origin: 'HomieOrigin',
    ) -> Optional[Type['HomieThread']]:
        """
        Return the Homie class definition for its instantiation.

        :param origin: Child class instance for Homie Automate.
        :returns: Homie class definition for its instantiation.
        """

        family = origin.family

        if family == 'philips':
            return PhueStream

        return None
