"""
Functions and routines associated with Enasis Network Homie Automate.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from typing import Literal
from typing import TYPE_CHECKING

from encommon.times import Time
from encommon.times import Timer
from encommon.types import NCFalse

from .child import HomieChild
from .helpers import occurd
from .helpers import whered
from ..models import HomieModels
from ..plugins import HomieOccur
from ..plugins import HomieWhere

if TYPE_CHECKING:
    from .device import HomieDevice
    from .group import HomieGroup
    from ..params import HomieAspireParams
    from ..threads import HomieStreamItem



class HomieAspire(HomieChild):
    """
    Match specific conditions for determining desired state.
    """

    __occurs: list[HomieOccur]
    __wheres: list[HomieWhere]

    __timer: Timer


    def __post__(
        self,
    ) -> None:
        """
        Initialize instance for class using provided parameters.
        """

        self.__occurs = []
        self.__wheres = []

        self.__build_occurs()
        self.__build_wheres()


        params = self.params

        timer = Timer(
            params.pause,
            start='min')

        self.__timer = timer


    def __build_occurs(
        self,
    ) -> None:
        """
        Construct instances using the configuration parameters.
        """

        params = self.params
        occurs = params.occurs
        homie = self.homie

        if occurs is None:
            return None

        model = HomieOccur


        plugins: list[HomieOccur] = []


        for occur in occurs:

            object = model(
                homie, occur)

            plugins.append(object)


        self.__occurs = plugins


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

        occurs = self.__occurs

        for occur in occurs:
            occur.validate()

        wheres = self.__wheres

        for where in wheres:
            where.validate()


    @property
    def kind(
        self,
    ) -> Literal['aspire']:
        """
        Return the value for the attribute from class instance.

        :returns: Value for the attribute from class instance.
        """

        return 'aspire'


    @property
    def params(
        self,
    ) -> 'HomieAspireParams':
        """
        Return the Pydantic model containing the configuration.

        :returns: Pydantic model containing the configuration.
        """

        model = (
            HomieModels
            .aspire())

        params = super().params

        assert isinstance(
            params, model)

        return params


    @property
    def devices(
        self,
    ) -> list['HomieDevice']:
        """
        Return the value for the attribute from class instance.

        .. note::
           This method is identical to same within HomieDesire.

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
           This method is identical to same within HomieDesire.

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
    def occurs(
        self,
    ) -> list[HomieOccur]:
        """
        Return the value for the attribute from class instance.

        :returns: Value for the attribute from class instance.
        """

        return list(self.__occurs)


    @property
    def wheres(
        self,
    ) -> list[HomieWhere]:
        """
        Return the value for the attribute from class instance.

        :returns: Value for the attribute from class instance.
        """

        return list(self.__wheres)


    def when(  # noqa: CFQ004
        self,
        sitem: 'HomieStreamItem',
    ) -> bool:
        """
        Return the boolean indicating the conditional outcomes.

        .. note::
           Somewhat similar to same method within HomieDesire.

        :param sitem: Item containing information for operation.
        :returns: Boolean indicating the conditional outcomes.
        """

        homie = self.homie

        time = Time('now')


        def _whered() -> bool:

            wheres = (
                whered(self, time))

            if len(wheres) >= 1:
                return all(wheres)

            return True


        def _occurd() -> bool:

            occurs = (
                occurd(self, sitem))

            if len(occurs) >= 1:
                return any(occurs)

            return False


        try:

            wheres = _whered()
            occurs = _occurd()

            return wheres and occurs

        except Exception as reason:

            homie.logger.log_e(
                base=self,
                name=self,
                status='exception',
                exc_info=reason)

        return NCFalse


    @property
    def paused(
        self,
    ) -> bool:
        """
        Return the boolean indicating whether operation delayed.

        .. note::
           Somewhat similar to same method within HomieDesire.

        :returns: Boolean indicating whether operation delayed.
        """

        timer = self.__timer

        return timer.pause(False)


    def matched(
        self,
    ) -> None:
        """
        Perform operations when this desire is the most desired.

        .. note::
           Somewhat similar to same method within HomieDesire.
        """

        homie = self.homie
        timer = self.__timer

        if homie.dryrun:
            return None

        timer.update('now')
