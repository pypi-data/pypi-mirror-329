"""
Functions and routines associated with Enasis Network Homie Automate.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from threading import Event
from typing import Optional
from typing import TYPE_CHECKING
from typing import Type

from encommon.types import clsname

from ..addons import HomieQueue

if TYPE_CHECKING:
    from ..childs import HomieOrigin
    from ..homie import Homie
    from ..threads import HomieActionItem
    from ..threads import HomieStreamItem
    from ..threads import HomieThread
    from ..threads import HomieUpdateItem



HomieThreads = dict[str, 'HomieThread']

_CONGEST = list[tuple[str, int]]



class HomieMember:
    """
    Common methods and routines for Homie Automate members.

    :param homie: Primary class instance for Homie Automate.
    """

    __homie: 'Homie'

    __threads: HomieThreads

    __aqueue: HomieQueue['HomieActionItem']
    __uqueue: HomieQueue['HomieUpdateItem']
    __squeue: HomieQueue['HomieStreamItem']
    __vacate: Event
    __cancel: Event


    def __init__(
        self,
        homie: 'Homie',
    ) -> None:
        """
        Initialize instance for class using provided parameters.
        """

        homie.logger.log_d(
            base=self,
            status='initial')

        self.__homie = homie

        self.__threads = {}

        self.__build_objects()

        self.__post__()

        homie.logger.log_i(
            base=self,
            status='created')


    def __post__(
        self,
    ) -> None:
        """
        Initialize instance for class using provided parameters.
        """


    def __build_objects(
        self,
    ) -> None:
        """
        Construct instances using the configuration parameters.
        """

        homie = self.__homie

        self.__aqueue = (
            HomieQueue(homie))

        self.__uqueue = (
            HomieQueue(homie))

        self.__squeue = (
            HomieQueue(homie))

        self.__vacate = Event()
        self.__cancel = Event()

        self.__build_threads()


    def __build_threads(
        self,
    ) -> None:
        """
        Construct instances using the configuration parameters.
        """

        homie = self.__homie
        childs = homie.childs
        origins = childs.origins


        threads: 'HomieThreads' = {}


        items = origins.items()

        for name, origin in items:

            thread = (
                self
                .get_thread(origin))

            if thread is None:
                continue

            object = thread(
                self, origin)

            threads[name] = object


        self.__threads = threads


    @property
    def homie(
        self,
    ) -> 'Homie':
        """
        Return the Homie instance to which the instance belongs.

        :returns: Homie instance to which the instance belongs.
        """

        return self.__homie


    @property
    def threads(
        self,
    ) -> HomieThreads:
        """
        Return the value for the attribute from class instance.

        :returns: Value for the attribute from class instance.
        """

        threads = self.__threads

        return dict(threads)


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


    @property
    def vacate(
        self,
    ) -> Event:
        """
        Return the value for the attribute from class instance.

        :returns: Value for the attribute from class instance.
        """

        return self.__vacate


    @property
    def cancel(
        self,
    ) -> Event:
        """
        Return the value for the attribute from class instance.

        :returns: Value for the attribute from class instance.
        """

        return self.__cancel


    @property
    def running(
        self,
    ) -> list[str]:
        """
        Return the list of threads which are determined running.

        :returns: List of threads which are determined running.
        """

        running: list[str] = []

        threads = (
            self.__threads
            .values())

        for thread in threads:

            if not thread.is_alive():
                continue

            name = thread.name

            running.append(name)

        return sorted(running)


    @property
    def zombies(
        self,
    ) -> list[str]:
        """
        Return the list of threads which are determined zombies.

        :returns: List of threads which are determined zombies.
        """

        zombies: list[str] = []

        threads = (
            self.__threads
            .values())

        for thread in threads:

            if thread.is_alive():
                continue

            name = thread.name

            zombies.append(name)

        return sorted(zombies)


    @property
    def congest(
        self,
    ) -> _CONGEST:
        """
        Return the list of congested threads and members queues.

        :returns: List of congested threads and members queues.
        """

        congest: _CONGEST = []

        name = clsname(self)

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


        threads = (
            self.__threads
            .values())

        for thread in threads:

            congest.extend(
                thread.congest)


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

        name = clsname(self)

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


        threads = (
            self.__threads
            .values())

        for thread in threads:

            enqueue.extend(
                thread.enqueue)


        return sorted(enqueue)


    def start(
        self,
    ) -> None:
        """
        Start the various threads within the Homie class object.
        """

        threads = (
            self.__threads
            .values())

        for thread in threads:
            thread.start()


    def operate(
        self,
    ) -> None:
        """
        Perform the operation related to Homie service members.
        """

        raise NotImplementedError


    def operate_updates(
        self,
    ) -> None:
        """
        Perform the operation related to Homie service members.
        """

        # Where the updates spread

        vacate = self.vacate
        uqueue = self.uqueue

        threads = (
            self.__threads
            .values())


        def _put_update() -> None:

            uqueue = thread.uqueue

            uqueue.put(uitem)


        while not uqueue.empty:

            uitem = uqueue.get()

            if vacate.is_set():
                continue

            for thread in threads:
                _put_update()


    def soft(
        self,
    ) -> None:
        """
        Stop the various threads within the Homie class object.
        """

        self.__vacate.set()


    def stop(
        self,
    ) -> None:
        """
        Stop the various threads within the Homie class object.
        """

        self.__cancel.set()

        threads = (
            self.__threads
            .values())

        for thread in threads:
            thread.stop()


    def get_thread(
        self,
        origin: 'HomieOrigin',
    ) -> Optional[Type['HomieThread']]:
        """
        Return the Homie class definition for its instantiation.

        :param origin: Child class instance for Homie Automate.
        :returns: Homie class definition for its instantiation.
        """

        raise NotImplementedError
