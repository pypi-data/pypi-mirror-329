"""
Functions and routines associated with Enasis Network Homie Automate.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from typing import Literal
from typing import TYPE_CHECKING
from typing import Type

from encommon.times import Time

from .plugin import HomiePlugin
from ..models import HomieModels
from ...utils import InvalidParam
from ...utils import UnexpectedCondition

if TYPE_CHECKING:
    from .driver import HomieDriver
    from ..params import HomieWhereParams



class HomieWhere(HomiePlugin):
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

        _bltn_store = params.builtins_store
        _bltn_period = params.builtins_period
        _phue_change = params.philips_change
        _ubiq_client = params.ubiquiti_client

        super().validate()


        enabled = [
            1 if _bltn_store else 0,
            1 if _bltn_period else 0,
            1 if _phue_change else 0,
            1 if _ubiq_client else 0]

        if sum(enabled) != 1:

            raise InvalidParam(
                error='minimal')


    @property
    def kind(
        self,
    ) -> Literal['where']:
        """
        Return the value for the attribute from class instance.

        :returns: Value for the attribute from class instance.
        """

        return 'where'


    @property
    def params(
        self,
    ) -> 'HomieWhereParams':
        """
        Return the Pydantic model containing the configuration.

        :returns: Pydantic model containing the configuration.
        """

        model = (
            HomieModels
            .where())

        params = super().params

        assert isinstance(
            params, model)

        return params


    def get_drivers(
        self,
    ) -> dict[str, Type['HomieDriver']]:
        """
        Return the Homie class definition for its instantiation.

        :returns: Homie class definition for its instantiation.
        """

        from ...builtins import (
            DriverBltnPeriod)

        from ...builtins import (
            DriverBltnStore)

        from ...philips import (
            DriverPhueChange)

        from ...ubiquiti import (
            DriverUbiqClient)


        return {

            'builtins_period': (
                DriverBltnPeriod),

            'builtins_store': (
                DriverBltnStore),

            'philips_change': (
                DriverPhueChange),

            'ubiquiti_client': (
                DriverUbiqClient)}


    def when(
        self,
        time: Time,
    ) -> bool:
        """
        Return the boolean indicating the conditional outcomes.

        .. note::
           Somewhat similar to same method within HomieOccur.

        :param time: Time that will be used in the conditionals.
        :returns: Boolean indicating the conditional outcomes.
        """

        drivers = self.drivers

        wheres: list[bool] = []


        for driver in drivers:

            where = driver.where(time)

            wheres.append(where)


        if len(wheres) >= 1:
            return all(wheres)

        raise UnexpectedCondition
