"""
Functions and routines associated with Enasis Network Homie Automate.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from dataclasses import dataclass
from threading import Thread
from time import sleep as block_sleep
from typing import TYPE_CHECKING

from encommon.types import clsname

from ..addons import HomieQueue
from ..addons import HomieQueueItem

if TYPE_CHECKING:
    from ..childs import HomieOrigin
    from ..homie import Homie
    from ..members import HomieMember
    from ..threads import HomieActionItem
    from ..threads import HomieStreamItem
    from ..threads import HomieUpdateItem



_UPDATES = dict[
    'HomieOrigin',
    'HomieUpdateItem']

_CONGEST = list[tuple[str, int]]



@dataclass
class HomieThreadItem(HomieQueueItem):
    """
    Contain information for sharing using the Python queue.
    """

    origin: str


    def __init__(
        self,
        origin: 'HomieOrigin',
    ) -> None:
        """
        Initialize instance for class using provided parameters.
        """

        self.origin = origin.name

        super().__init__()



class HomieThread(Thread):
    """
    Common methods and routines for Homie Automate threads.

    :param member: Child class instance for Homie Automate.
    :param origin: Child class instance for Homie Automate.
    """

    __member: 'HomieMember'
    __origin: 'HomieOrigin'

    __aqueue: HomieQueue['HomieActionItem']
    __uqueue: HomieQueue['HomieUpdateItem']
    __squeue: HomieQueue['HomieStreamItem']


    def __init__(
        self,
        member: 'HomieMember',
        origin: 'HomieOrigin',
    ) -> None:
        """
        Initialize instance for class using provided parameters.
        """

        homie = member.homie

        super().__init__()

        self.name = (
            f'{clsname(self)}'
            f'/{origin.name}')

        homie.logger.log_d(
            base=self,
            name=origin,
            status='initial')

        self.__member = member
        self.__origin = origin

        self.__build_objects()

        homie.logger.log_i(
            base=self,
            name=origin,
            status='created')


    def __build_objects(
        self,
    ) -> None:
        """
        Construct instances using the configuration parameters.
        """

        member = self.__member
        homie = member.homie

        self.__aqueue = (
            HomieQueue(homie))

        self.__uqueue = (
            HomieQueue(homie))

        self.__squeue = (
            HomieQueue(homie))


    @property
    def homie(
        self,
    ) -> 'Homie':
        """
        Return the Homie instance to which the instance belongs.

        :returns: Homie instance to which the instance belongs.
        """

        return self.member.homie


    @property
    def member(
        self,
    ) -> 'HomieMember':
        """
        Return the value for the attribute from class instance.

        :returns: Value for the attribute from class instance.
        """

        return self.__member


    @property
    def origin(
        self,
    ) -> 'HomieOrigin':
        """
        Return the value for the attribute from class instance.

        :returns: Value for the attribute from class instance.
        """

        return self.__origin


    @property
    def aqueue(
        self,
    ) -> HomieQueue['HomieActionItem']:
        """
        Return the value for the attribute from class instance.

        :returns: Value for the attribute from class instance.
        """

        return self.__aqueue


    @property
    def uqueue(
        self,
    ) -> HomieQueue['HomieUpdateItem']:
        """
        Return the value for the attribute from class instance.

        :returns: Value for the attribute from class instance.
        """

        return self.__uqueue


    @property
    def squeue(
        self,
    ) -> HomieQueue['HomieStreamItem']:
        """
        Return the value for the attribute from class instance.

        :returns: Value for the attribute from class instance.
        """

        return self.__squeue


    def expired(
        self,
        item: HomieThreadItem,
    ) -> bool:
        """
        Return the boolean indicating whether the item expired.

        :param item: Item containing information for operation.
        :returns: Boolean indicating whether the item expired.
        """

        member = self.member
        homie = member.homie

        since = item.time.since
        origin = item.origin

        if since < 60:
            return False

        homie.logger.log_w(
            base=self,
            item=item,
            origin=origin,
            status='expired',
            age=int(since))

        return True


    @property
    def congest(
        self,
    ) -> _CONGEST:
        """
        Return the list of congested threads and members queues.

        :returns: List of congested threads and members queues.
        """

        congest: _CONGEST = []

        name = self.name

        aqueue = self.aqueue
        uqueue = self.uqueue
        squeue = self.squeue


        if aqueue.qsize > 5:

            append = (
                f'{name}/aqueue',
                aqueue.qsize)

            congest.append(append)

        if uqueue.qsize > 5:

            append = (
                f'{name}/uqueue',
                uqueue.qsize)

            congest.append(append)

        if squeue.qsize > 5:

            append = (
                f'{name}/squeue',
                squeue.qsize)

            congest.append(append)


        return sorted(congest)


    @property
    def enqueue(
        self,
    ) -> _CONGEST:
        """
        Return the list of congested threads and members queues.

        :returns: List of congested threads and members queues.
        """

        enqueue: _CONGEST = []

        name = self.name

        aqueue = self.aqueue
        uqueue = self.uqueue
        squeue = self.squeue


        if aqueue.qsize > 0:

            append = (
                f'{name}/aqueue',
                aqueue.qsize)

            enqueue.append(append)

        if uqueue.qsize > 0:

            append = (
                f'{name}/uqueue',
                uqueue.qsize)

            enqueue.append(append)

        if squeue.qsize > 0:

            append = (
                f'{name}/squeue',
                squeue.qsize)

            enqueue.append(append)


        return sorted(enqueue)


    def run(
        self,
    ) -> None:
        """
        Perform whatever operation is associated with the class.
        """

        member = self.__member
        origin = self.__origin
        homie = member.homie
        vacate = member.vacate
        cancel = member.cancel

        homie.logger.log_i(
            base=self,
            name=origin,
            status='started')


        def _continue() -> bool:

            if cancel.is_set():
                return False

            enqueue = bool(
                self.enqueue)

            if vacate.is_set():
                return enqueue

            return True


        while _continue():

            self.operate_updates()

            self.operate()

            block_sleep(0.1)


        homie.logger.log_i(
            base=self,
            name=origin,
            status='stopped')


    def operate(
        self,
    ) -> None:
        """
        Perform the operation related to Homie service threads.
        """

        raise NotImplementedError


    def operate_updates(
        self,
    ) -> None:
        """
        Perform the operation related to Homie service threads.
        """

        member = self.__member
        homie = member.homie
        childs = homie.childs

        vacate = member.vacate
        uqueue = self.__uqueue

        origins = (
            childs.origins
            .values())


        updates: _UPDATES = {}


        def _set_update() -> None:

            name = uitem.origin
            _name = origin.name

            if name != _name:
                return None

            updates[origin] = uitem


        while not uqueue.empty:

            uitem = uqueue.get()

            if vacate.is_set():
                continue

            if self.expired(uitem):
                continue

            for origin in origins:
                _set_update()


        items = updates.items()

        for origin, uitem in items:

            (origin
             .set_update(uitem))


    def stop(
        self,
    ) -> None:
        """
        Wait for the thread object to complete routine and exit.
        """

        member = self.__member
        origin = self.__origin
        homie = member.homie

        homie.logger.log_d(
            base=self,
            name=origin,
            status='waiting')

        self.join()

        homie.logger.log_d(
            base=self,
            name=origin,
            status='awaited')
