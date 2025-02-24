"""
Functions and routines associated with Enasis Network Homie Automate.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from typing import Literal
from typing import TYPE_CHECKING
from typing import Type

from .plugin import HomiePlugin
from ..models import HomieModels
from ...utils import InvalidParam
from ...utils import UnexpectedCondition

if TYPE_CHECKING:
    from .driver import HomieDriver
    from ..params import HomieOccurParams
    from ..threads import HomieStreamItem



class HomieOccur(HomiePlugin):
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

        _bltn_regexp = params.builtins_regexp
        _phue_button = params.philips_button
        _phue_contact = params.philips_contact
        _phue_motion = params.philips_motion
        _phue_scene = params.philips_scene

        super().validate()


        enabled = [
            1 if _bltn_regexp else 0,
            1 if _phue_button else 0,
            1 if _phue_contact else 0,
            1 if _phue_motion else 0,
            1 if _phue_scene else 0]

        if sum(enabled) != 1:

            raise InvalidParam(
                error='minimal')


    @property
    def kind(
        self,
    ) -> Literal['occur']:
        """
        Return the value for the attribute from class instance.

        :returns: Value for the attribute from class instance.
        """

        return 'occur'


    @property
    def params(
        self,
    ) -> 'HomieOccurParams':
        """
        Return the Pydantic model containing the configuration.

        :returns: Pydantic model containing the configuration.
        """

        model = (
            HomieModels
            .occur())

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
            DriverBltnRegexp)

        from ...philips import (
            DriverPhueButton)

        from ...philips import (
            DriverPhueContact)

        from ...philips import (
            DriverPhueMotion)

        from ...philips import (
            DriverPhueScene)


        return {

            'builtins_regexp': (
                DriverBltnRegexp),

            'philips_button': (
                DriverPhueButton),

            'philips_contact': (
                DriverPhueContact),

            'philips_motion': (
                DriverPhueMotion),

            'philips_scene': (
                DriverPhueScene)}


    def when(
        self,
        sitem: 'HomieStreamItem',
    ) -> bool:
        """
        Return the boolean indicating the conditional outcomes.

        .. note::
           Somewhat similar to same method within HomieWhere.

        :param sitem: Item containing information for operation.
        :returns: Boolean indicating the conditional outcomes.
        """

        drivers = self.drivers

        occurs: list[bool] = []


        for driver in drivers:

            occur = driver.occur(sitem)

            occurs.append(occur)


        if len(occurs) >= 1:
            return any(occurs)

        raise UnexpectedCondition
