"""
Functions and routines associated with Enasis Network Homie Automate.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from dataclasses import dataclass
from queue import Queue
from typing import Generic
from typing import TYPE_CHECKING
from typing import TypeVar

from encommon.times import Time

if TYPE_CHECKING:
    from ..homie import Homie



HomieQueueItemType = TypeVar('HomieQueueItemType')



@dataclass
class HomieQueueItem:
    """
    Contain information for sharing using the Python queue.
    """

    time: Time


    def __init__(
        self,
    ) -> None:
        """
        Initialize instance for class using provided parameters.
        """

        self.time = Time()



class HomieQueue(Generic[HomieQueueItemType]):
    """
    Queue object that will allow to handle full conditions.

    :param homie: Primary class instance for Homie Automate.
    :param size: Maximum size for the created queue object.
    """

    __homie: 'Homie'

    __queue: Queue[HomieQueueItemType]


    def __init__(
        self,
        homie: 'Homie',
        size: int = 10000,
    ) -> None:
        """
        Initialize instance for class using provided parameters.
        """

        self.__homie = homie

        self.__queue = Queue(size)


    @property
    def empty(
        self,
    ) -> bool:
        """
        Return the boolean indicating whether the queue is full.

        :returns: Boolean indicating whether the queue is full.
        """

        queue = self.__queue

        return queue.empty()


    @property
    def qsize(
        self,
    ) -> int:
        """
        Return the value for the attribute from class instance.

        :returns: Value for the attribute from class instance.
        """

        queue = self.__queue

        return queue.qsize()


    def put(
        self,
        item: HomieQueueItemType,
    ) -> None:
        """
        Store the provided item within the queue class instance.

        :param item: Item containing information for operation.
        """

        homie = self.__homie
        queue = self.__queue

        try:
            queue.put(item, False)

        except Exception as reason:

            homie.logger.log_e(
                base=self,
                status='exception',
                exc_info=reason)


    def get(
        self,
    ) -> HomieQueueItemType:
        """
        Return the next item within the queue in blocking mode.

        :returns: Next item within the queue in blocking mode.
        """

        queue = self.__queue

        return queue.get()
