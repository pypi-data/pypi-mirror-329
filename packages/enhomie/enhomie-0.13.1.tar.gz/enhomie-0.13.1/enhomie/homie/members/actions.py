"""
Functions and routines associated with Enasis Network Homie Automate.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from typing import Optional
from typing import TYPE_CHECKING
from typing import Type

from encommon.times import Time
from encommon.times import Timer

from .member import HomieMember
from ...hubitat import HubiAction
from ...philips import PhueAction

if TYPE_CHECKING:
    from ..common import HomieState
    from ..childs import HomieOrigin
    from ..childs import HomieScene
    from ..threads import HomieActionNode
    from ..threads import HomieThread



class HomieActions(HomieMember):
    """
    Common methods and routines for Homie Automate members.
    """

    __timer: Timer


    def __post__(
        self,
    ) -> None:
        """
        Initialize instance for class using provided parameters.
        """

        homie = self.homie
        params = homie.params

        respite = (
            params.service
            .respite)

        timer = Timer(
            respite.desire,
            start='min')

        self.__timer = timer


    def operate(
        self,
    ) -> None:
        """
        Perform the operation related to Homie service members.
        """

        homie = self.homie

        self.operate_updates()


        try:
            self.operate_desires()
            self.operate_actions()

        except Exception as reason:

            homie.logger.log_e(
                base=self,
                item='desired',
                status='exception',
                exc_info=reason)


        try:
            self.operate_aspires()
            self.operate_actions()

        except Exception as reason:

            homie.logger.log_e(
                base=self,
                item='aspired',
                status='exception',
                exc_info=reason)


    def operate_desires(
        self,
    ) -> None:
        """
        Perform the operation related to Homie service members.
        """

        homie = self.homie
        desired = homie.desired
        timer = self.__timer


        if timer.pause():
            return None

        vacate = self.vacate

        if vacate.is_set():
            return None


        def _execute() -> None:

            homie.printer(aitem)

            self.put_actions(
                aitem.target,
                state=aitem.state,
                color=aitem.color,
                level=aitem.level,
                scene=aitem.scene)


        homie.logger.log_d(
            base=self,
            item='desired',
            status='started')

        time = Time('now')

        aitems = (
            desired.items(time))

        for aitem in aitems:
            _execute()

        homie.logger.log_d(
            base=self,
            item='desired',
            count=len(aitems),
            status='complete',
            elapsed=time)


    def operate_aspires(
        self,
    ) -> None:
        """
        Perform the operation related to Homie service members.
        """

        homie = self.homie
        aspired = homie.aspired

        vacate = self.vacate
        squeue = self.squeue


        def _execute() -> None:

            homie.printer(aitem)

            self.put_actions(
                aitem.target,
                state=aitem.state,
                color=aitem.color,
                level=aitem.level,
                scene=aitem.scene)


        while not squeue.empty:

            sitem = squeue.get()

            if vacate.is_set():
                continue

            aitems = (
                aspired.items(sitem))

            for aitem in aitems:
                _execute()


    def operate_actions(
        self,
    ) -> None:
        """
        Perform the operation related to Homie service members.
        """

        # Where the actions process

        homie = self.homie
        childs = homie.childs
        origins = childs.origins
        vacate = self.vacate
        aqueue = self.aqueue

        threads = (
            self.threads
            .values())


        def _put_action() -> None:

            origin = thread.origin
            _name = origin.name

            if name != _name:
                return None

            (thread
             .aqueue.put(aitem))


        while not aqueue.empty:

            aitem = aqueue.get()

            if vacate.is_set():
                continue

            origin = origins[
                aitem.origin]

            name = origin.name

            for thread in threads:
                _put_action()

            homie.printer(aitem)


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

        if family == 'hubitat':
            return HubiAction

        if family == 'philips':
            return PhueAction

        return None


    def put_actions(
        self,
        target: 'HomieActionNode',
        *,
        state: Optional['HomieState'] = None,
        color: Optional[str] = None,
        level: Optional[int] = None,
        scene: Optional['HomieScene'] = None,
    ) -> None:
        """
        Insert the new item containing information for operation.

        :param target: Device or group settings will be updated.
        :param state: Determine the state related to the target.
        :param color: Determine the color related to the target.
        :param level: Determine the level related to the target.
        :param scene: Determine the scene related to the target.
        """

        homie = self.homie
        aqueue = self.aqueue

        aitems = (
            homie.get_actions(
                target=target,
                state=state,
                color=color,
                level=level,
                scene=scene))

        items = aitems.items()

        for target, aitem in items:

            origin = target.origin

            assert origin is not None

            origin.put_action(
                aqueue=aqueue,
                target=target,
                state=aitem.state,
                color=aitem.color,
                level=aitem.level,
                scene=aitem.scene)
