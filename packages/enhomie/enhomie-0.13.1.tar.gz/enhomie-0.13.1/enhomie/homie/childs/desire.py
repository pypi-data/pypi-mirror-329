"""
Functions and routines associated with Enasis Network Homie Automate.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from typing import Literal
from typing import Optional
from typing import TYPE_CHECKING

from encommon.times import Time
from encommon.times import TimerParams
from encommon.times import Timers
from encommon.times import TimersParams
from encommon.times.params import _TIMERS

from .child import HomieChild
from .helpers import whered
from ..models import HomieModels
from ..plugins import HomieWhere

if TYPE_CHECKING:
    from .device import HomieDevice
    from .group import HomieGroup
    from ..params import HomieDesireParams
    from ..threads import HomieActionNode



class HomieDesire(HomieChild):
    """
    Match specific conditions for determining desired state.
    """

    __wheres: list[HomieWhere]

    __timers: Timers


    def __post__(
        self,
    ) -> None:
        """
        Initialize instance for class using provided parameters.
        """

        self.__wheres = []

        self.__build_wheres()
        self.__build_timers()


    def __build_timers(
        self,
    ) -> None:
        """
        Construct instances using the configuration parameters.
        """

        homie = self.homie
        params = self.params

        timers: _TIMERS = {}

        pause = params.pause
        delay = params.delay

        store = (
            homie.params
            .database)

        _model = TimerParams
        model = TimersParams


        start = (
            'now'
            if delay is True
            else 'min')


        names = params.devices

        for name in names or []:

            unique = f'device/{name}'

            timer = _model(
                timer=pause,
                start=start)

            timers[unique] = timer


        names = params.groups

        for name in names or []:

            unique = f'group/{name}'

            timer = _model(
                timer=pause,
                start=start)

            timers[unique] = timer


        name = self.name
        group = f'desire/{name}'

        object = Timers(
            model(timers),
            store=store,
            group=group)

        self.__timers = object



    def __build_wheres(
        self,
    ) -> None:
        """
        Construct instances using the configuration parameters.
        """

        params = self.params
        wheres = params.wheres
        homie = self.homie

        if wheres is None:
            return None

        model = HomieWhere


        plugins: list[HomieWhere] = []


        for where in wheres:

            object = model(
                homie, where)

            plugins.append(object)


        self.__wheres = plugins


    def validate(
        self,
    ) -> None:
        """
        Perform advanced validation on the parameters provided.
        """

        wheres = self.__wheres

        for where in wheres:
            where.validate()


    @property
    def kind(
        self,
    ) -> Literal['desire']:
        """
        Return the value for the attribute from class instance.

        :returns: Value for the attribute from class instance.
        """

        return 'desire'


    @property
    def params(
        self,
    ) -> 'HomieDesireParams':
        """
        Return the Pydantic model containing the configuration.

        :returns: Pydantic model containing the configuration.
        """

        model = (
            HomieModels
            .desire())

        params = super().params

        assert isinstance(
            params, model)

        return params


    @property
    def weight(
        self,
    ) -> int:
        """
        Return the value for the attribute from class instance.

        :returns: Value for the attribute from class instance.
        """

        return self.params.weight


    @property
    def devices(
        self,
    ) -> list['HomieDevice']:
        """
        Return the value for the attribute from class instance.

        .. note::
           This method is identical to same within HomieAspire.

        :returns: Value for the attribute from class instance.
        """

        params = self.params
        names = params.devices

        devices = (
            self.homie.childs
            .devices)

        childs: set['HomieDevice'] = set()

        if names is None:
            return list(childs)

        for name in names:

            child = devices[name]

            childs.add(child)

        return list(childs)


    @property
    def groups(
        self,
    ) -> list['HomieGroup']:
        """
        Return the value for the attribute from class instance.

        .. note::
           This method is identical to same within HomieAspire.

        :returns: Value for the attribute from class instance.
        """

        params = self.params
        names = params.groups

        groups = (
            self.homie.childs
            .groups)

        childs: set['HomieGroup'] = set()

        if names is None:
            return list(childs)

        for name in names:

            child = groups[name]

            childs.add(child)

        return list(childs)


    @property
    def wheres(
        self,
    ) -> list[HomieWhere]:
        """
        Return the value for the attribute from class instance.

        :returns: Value for the attribute from class instance.
        """

        return list(self.__wheres)


    def when(
        self,
        time: Time,
    ) -> bool:
        """
        Return the boolean indicating the conditional outcomes.

        .. note::
           Somewhat similar to same method within HomieAspire.

        :param time: Time that will be used in the conditionals.
        :returns: Boolean indicating the conditional outcomes.
        """

        homie = self.homie

        try:

            wheres = (
                whered(self, time))

            if len(wheres) >= 1:
                return all(wheres)

        except Exception as reason:

            homie.logger.log_e(
                base=self,
                name=self,
                status='exception',
                exc_info=reason)

        return False


    def paused(
        self,
        target: 'HomieActionNode',
    ) -> bool:
        """
        Return the boolean indicating whether operation delayed.

        .. note::
           This method is identical to same within HomieAspire.

        :param target: Device or group that in scope for match.
        :returns: Boolean indicating whether operation delayed.
        """

        timers = self.__timers

        name = target.name
        kind = target.kind

        ready = timers.ready(
            f'{kind}/{name}',
            update=False)

        return ready is False


    def matched(
        self,
        target: 'HomieActionNode',
    ) -> None:
        """
        Perform operations when this desire is the most desired.

        .. note::
           Somewhat similar to same method within HomieAspire.

        :param target: Device or group that in scope for match.
        """

        homie = self.homie
        timers = self.__timers

        if homie.dryrun:
            return None

        name = target.name
        kind = target.kind

        timers.update(
            f'{kind}/{name}',
            value='now')


    def omitted(
        self,
        target: Optional['HomieActionNode'] = None,
    ) -> None:
        """
        Perform operations when this desire is the most desired.

        .. note::
           Somewhat similar to same method within HomieAspire.

        :param target: Device or group that in scope for match.
        """

        homie = self.homie
        timers = self.__timers
        params = self.params
        delay = params.delay

        if homie.dryrun:
            return None

        update = (
            'now'
            if delay is True
            else 'min')


        if target is None:

            _timers = (
                timers.children
                .values())

            for timer in _timers:
                timer.update(update)


        elif target is not None:

            name = target.name
            kind = target.kind

            timers.update(
                f'{kind}/{name}',
                value=update)
