"""
Functions and routines associated with Enasis Network Homie Automate.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from threading import Event
from time import sleep as block_sleep
from typing import Any
from typing import Optional
from typing import TYPE_CHECKING

from encommon.times import Timer

from .members import HomieActions
from .members import HomieRestful
from .members import HomieStreams
from .members import HomieUpdates

if TYPE_CHECKING:
    from .homie import Homie
    from .params import HomieServiceParams



_CONGEST = list[tuple[str, int]]



class HomieService:
    """
    Multi-threaded service for processing the desired state.

    :param homie: Primary class instance for Homie Automate.
    """

    __homie: 'Homie'

    __actions: Optional[HomieActions]
    __updates: Optional[HomieUpdates]
    __streams: Optional[HomieStreams]
    __restful: Optional[HomieRestful]

    __timer: Timer
    __vacate: Event
    __cancel: Event
    __started: bool


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

        self.__build_objects()

        self.__started = False

        homie.logger.log_i(
            base=self,
            status='created')


    def __build_objects(
        self,
    ) -> None:
        """
        Construct instances using the configuration parameters.
        """

        homie = self.__homie
        params = self.params

        respite = params.respite
        members = params.members


        self.__actions = (
            HomieActions(homie)
            if members.actions
            else None)

        self.__updates = (
            HomieUpdates(homie)
            if members.updates
            else None)

        self.__streams = (
            HomieStreams(homie)
            if members.streams
            else None)

        self.__restful = (
            HomieRestful(homie)
            if members.restful
            else None)


        self.__timer = Timer(
            respite.health,
            start='min')

        self.__vacate = Event()
        self.__cancel = Event()


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
    def params(
        self,
    ) -> 'HomieServiceParams':
        """
        Return the Pydantic model containing the configuration.

        :returns: Pydantic model containing the configuration.
        """

        homie = self.__homie
        params = homie.params

        return params.service


    @property
    def actions(
        self,
    ) -> Optional[HomieActions]:
        """
        Return the value for the attribute from class instance.

        :returns: Value for the attribute from class instance.
        """

        return self.__actions


    @property
    def updates(
        self,
    ) -> Optional[HomieUpdates]:
        """
        Return the value for the attribute from class instance.

        :returns: Value for the attribute from class instance.
        """

        return self.__updates


    @property
    def streams(
        self,
    ) -> Optional[HomieStreams]:
        """
        Return the value for the attribute from class instance.

        :returns: Value for the attribute from class instance.
        """

        return self.__streams


    @property
    def restful(
        self,
    ) -> Optional[HomieRestful]:
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

        running: list[str] = []

        actions = self.__actions
        updates = self.__updates
        streams = self.__streams
        restful = self.__restful

        if actions is not None:
            running.extend(
                actions.running)

        if updates is not None:
            running.extend(
                updates.running)

        if streams is not None:
            running.extend(
                streams.running)

        if restful is not None:
            running.extend(
                restful.running)

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

        actions = self.__actions
        updates = self.__updates
        streams = self.__streams
        restful = self.__restful

        if actions is not None:
            zombies.extend(
                actions.zombies)

        if updates is not None:
            zombies.extend(
                updates.zombies)

        if streams is not None:
            zombies.extend(
                streams.zombies)

        if restful is not None:
            zombies.extend(
                restful.zombies)

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

        actions = self.__actions
        updates = self.__updates
        streams = self.__streams
        restful = self.__restful

        if actions is not None:
            congest.extend(
                actions.congest)

        if updates is not None:
            congest.extend(
                updates.congest)

        if streams is not None:
            congest.extend(
                streams.congest)

        if restful is not None:
            congest.extend(
                restful.congest)

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

        actions = self.__actions
        updates = self.__updates
        streams = self.__streams
        restful = self.__restful

        if actions is not None:
            enqueue.extend(
                actions.enqueue)

        if updates is not None:
            enqueue.extend(
                updates.enqueue)

        if streams is not None:
            enqueue.extend(
                streams.enqueue)

        if restful is not None:
            enqueue.extend(
                restful.enqueue)

        return sorted(enqueue)


    def start(
        self,
    ) -> None:
        """
        Start the various threads within the Homie class object.
        """

        homie = self.__homie
        started = self.__started

        if started is True:
            return None

        actions = self.__actions
        updates = self.__updates
        streams = self.__streams
        restful = self.__restful

        self.__started = True

        homie.logger.log_i(
            base=self,
            status='starting')

        assert homie.refresh()


        if streams is not None:
            streams.start()

        if updates is not None:
            updates.start()

        if actions is not None:
            actions.start()

        if restful is not None:
            restful.start()


        homie.logger.log_i(
            base=self,
            status='started')


    def operate(
        self,
    ) -> None:
        """
        Perform the operation related to Homie service members.
        """

        homie = self.__homie

        actions = self.__actions
        updates = self.__updates
        streams = self.__streams
        restful = self.__restful

        while self.running:

            if updates is not None:
                updates.operate()

            self.operate_updates()
            self.operate_streams()

            if actions is not None:
                actions.operate()

            if streams is not None:
                streams.operate()

            if restful is not None:
                restful.operate()

            block_sleep(0.05)

            self.operate_healths()

        homie.logger.log_i(
            base=self,
            status='vacated')


    def operate_updates(
        self,
    ) -> None:
        """
        Perform the operation related to Homie service members.
        """

        homie = self.__homie
        childs = homie.childs

        vacate = self.__vacate
        actions = self.__actions
        updates = self.__updates

        if updates is None:
            return None

        uqueue = updates.uqueue

        auqueue = (
            actions.uqueue
            if actions is not None
            else None)

        origins = (
            childs.origins
            .values())


        def _set_update() -> None:

            name = uitem.origin
            _name = origin.name

            if name != _name:
                return None

            (origin
             .set_update(uitem))


        while not uqueue.empty:

            uitem = uqueue.get()

            if vacate.is_set():
                continue

            if auqueue is not None:
                auqueue.put(uitem)

            for origin in origins:
                _set_update()

            homie.printer(uitem)


    def operate_streams(
        self,
    ) -> None:
        """
        Perform the operation related to Homie service members.
        """

        homie = self.__homie

        vacate = self.__vacate
        actions = self.__actions
        updates = self.__updates
        streams = self.__streams

        if streams is None:
            return None

        squeue = streams.squeue

        asqueue = (
            actions.squeue
            if actions is not None
            else None)

        usqueue = (
            updates.squeue
            if updates is not None
            else None)


        while not squeue.empty:

            sitem = squeue.get()

            if vacate.is_set():
                continue

            if asqueue is not None:
                asqueue.put(sitem)

            if usqueue is not None:
                usqueue.put(sitem)

            homie.printer(sitem)


    def operate_healths(
        self,
    ) -> None:
        """
        Perform the operation related to Homie service members.
        """

        timer = self.__timer

        if timer.pause():
            return None

        vacate = self.__vacate
        cancel = self.__cancel

        self.check_congest()

        if vacate.is_set():
            return None

        if cancel.is_set():
            return None

        if self.check_zombies():
            self.stop()


    def check_zombies(
        self,
    ) -> bool:
        """
        Return the boolean indicating while threads are zombies.

        :returns: Boolean indicating while threads are zombies.
        """

        homie = self.__homie
        zombies = self.zombies

        for name in zombies:

            homie.logger.log_c(
                thread=name,
                status='zombie')

        return len(zombies) != 0


    def check_congest(
        self,
    ) -> bool:
        """
        Return the boolean indicating when queues are congested.

        :returns: Boolean indicating when queues are congested.
        """

        homie = self.__homie
        congest = self.congest

        for name, count in congest:

            homie.logger.log_e(
                queue=name,
                status='congest',
                count=count)

        return len(congest) != 0


    def soft(
        self,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        """
        Stop the various threads within the Homie class object.

        :param kwargs: Keyword arguments ignored by the method.
        :param args: Positional arguments ignored by the method.
        """

        homie = self.__homie
        started = self.__started
        vacate = self.__vacate

        if started is False:
            return None

        if vacate.is_set():
            return self.stop()

        actions = self.__actions
        updates = self.__updates
        streams = self.__streams
        restful = self.__restful


        homie.logger.log_i(
            base=self,
            status='vacating')

        vacate.set()


        if streams is not None:
            streams.stop()

        if updates is not None:
            updates.soft()

        if actions is not None:
            actions.soft()

        if restful is not None:
            restful.soft()


    def stop(
        self,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        """
        Stop the various threads within the Homie class object.

        :param kwargs: Keyword arguments ignored by the method.
        :param args: Positional arguments ignored by the method.
        """

        homie = self.__homie
        started = self.__started
        cancel = self.__cancel

        if started is False:
            return None

        if cancel.is_set():
            return None

        actions = self.__actions
        updates = self.__updates
        streams = self.__streams
        restful = self.__restful


        cancel.set()

        homie.logger.log_i(
            base=self,
            status='stopping')


        if streams is not None:
            streams.stop()

        if updates is not None:
            updates.stop()

        if actions is not None:
            actions.stop()

        if restful is not None:
            restful.stop()


        homie.logger.log_i(
            base=self,
            status='stopped')
