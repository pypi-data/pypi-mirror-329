"""
Functions and routines associated with Enasis Network Homie Automate.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from typing import Literal
from typing import Optional
from typing import TYPE_CHECKING

from encommon.times import Time
from encommon.times import findtz

from .models import BltnModels
from ..homie.plugins import HomieDriver
from ..utils import InvalidParam

if TYPE_CHECKING:
    from .params import DriverBltnPeriodParams
    from ..homie.plugins import HomiePluginKinds



class DriverBltnPeriod(HomieDriver):
    """
    Match specific conditions for determining desired state.
    """


    def validate(
        self,
    ) -> None:
        """
        Perform advanced validation on the parameters provided.
        """

        params = self.params

        _start = params.start
        _stop = params.stop
        _tzname = params.tzname


        if (_start and _stop
                and _start >= _stop):

            raise InvalidParam(
                param='start',
                value=_start,
                error='invalid')


        tzinfo = findtz(_tzname)

        if tzinfo is None:

            raise InvalidParam(
                param='tzname',
                value=_tzname,
                error='invalid')


    @property
    def family(
        self,
    ) -> Literal['builtins']:
        """
        Return the value for the attribute from class instance.

        :returns: Value for the attribute from class instance.
        """

        return 'builtins'


    @property
    def kinds(
        self,
    ) -> list['HomiePluginKinds']:
        """
        Return the value for the attribute from class instance.

        :returns: Value for the attribute from class instance.
        """

        return ['where']


    @property
    def params(
        self,
    ) -> 'DriverBltnPeriodParams':
        """
        Return the Pydantic model containing the configuration.

        :returns: Pydantic model containing the configuration.
        """

        model = (
            BltnModels
            .drivers()
            .period())

        params = super().params

        assert isinstance(
            params, model)

        return params


    def where(  # noqa: CFQ004
        self,
        time: Time,
    ) -> bool:
        """
        Return the boolean indicating the conditional outcomes.

        :param time: Time that will be used in the conditionals.
        :returns: Boolean indicating the conditional outcomes.
        """

        params = self.params
        tzname = params.tzname

        start: Optional[Time] = None
        stop: Optional[Time] = None

        if tzname is not None:
            time = time.shifz(tzname)


        _time = Time(
            time.stamp('%H:%M'))

        today = time.stamp('%A')


        if params.start:

            start = Time(
                params.start,
                tzname=tzname)

            _start = Time(
                start.stamp('%H:%M'))

            if _time < _start:
                return False

        if params.stop:

            stop = Time(
                params.stop,
                tzname=tzname)

            _stop = Time(
                stop.stamp('%H:%M'))

            if _time > _stop:
                return False


        if params.days:

            days = params.days

            if today not in days:
                return False


        return True
