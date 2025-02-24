"""
Functions and routines associated with Enasis Network Homie Automate.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from threading import Thread
from typing import Optional
from typing import TYPE_CHECKING
from typing import Type

from .member import HomieMember
from ...restful import RestfulService

if TYPE_CHECKING:
    from ..childs import HomieOrigin
    from ..threads import HomieThread



class HomieRestful(HomieMember):
    """
    Common methods and routines for Homie Automate members.
    """

    __restful: RestfulService
    __thread: Thread


    def __post__(
        self,
    ) -> None:
        """
        Initialize instance for class using provided parameters.
        """

        homie = self.homie

        restful = (
            RestfulService(homie))

        restful.start()

        thread = Thread(
            target=restful.operate)

        thread.start()

        self.__restful = restful
        self.__thread = thread


    @property
    def restful(
        self,
    ) -> RestfulService:
        """
        Return the value for the attribute from class instance.

        :returns: Value for the attribute from class instance.
        """

        return self.__restful


    @property
    def running(
        self,
    ) -> list[str]:
        """
        Return the list of threads which are determined running.

        :returns: List of threads which are determined running.
        """

        thread = self.__thread
        running: list[str] = []

        if thread.is_alive():
            running.append('_restful')

        return running


    @property
    def zombies(
        self,
    ) -> list[str]:
        """
        Return the list of threads which are determined zombies.

        :returns: List of threads which are determined zombies.
        """

        thread = self.__thread
        zombies: list[str] = []

        if not thread.is_alive():
            zombies.append('_restful')

        return zombies


    def operate(
        self,
    ) -> None:
        """
        Perform the operation related to Homie service members.
        """

        # Nothing to do for member


    def operate_updates(
        self,
    ) -> None:
        """
        Perform the operation related to Homie service members.
        """

        # Nothing to do for member


    def soft(
        self,
    ) -> None:
        """
        Stop the various threads within the Homie class object.
        """

        super().soft()

        self.__restful.stop()
        self.__thread.join()


    def stop(
        self,
    ) -> None:
        """
        Stop the various threads within the Homie class object.
        """

        super().stop()

        self.__restful.stop()
        self.__thread.join()


    def get_thread(
        self,
        origin: 'HomieOrigin',
    ) -> Optional[Type['HomieThread']]:
        """
        Return the Homie class definition for its instantiation.

        :param origin: Child class instance for Homie Automate.
        :returns: Homie class definition for its instantiation.
        """

        # Nothing to do for member
