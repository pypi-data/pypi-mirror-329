"""
Functions and routines associated with Enasis Network Homie Automate.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from typing import Literal
from typing import TYPE_CHECKING
from typing import get_args

from encommon.types import NCFalse
from encommon.types import getate

from .helpers import phue_sensors
from ..models import PhueModels
from ..stream import PhueStreamItem
from ...homie.plugins import HomieDriver
from ...utils import InvalidParam

if TYPE_CHECKING:
    from ..params import DriverPhueMotionParams
    from ...homie.plugins import HomiePluginKinds
    from ...homie.threads import HomieStreamItem



PhueMotionState = Literal[
    'motion',
    'no_motion']

_STATES = list(
    get_args(PhueMotionState))



class DriverPhueMotion(HomieDriver):
    """
    Match specific conditions for determining desired state.
    """


    def validate(
        self,
    ) -> None:
        """
        Perform advanced validation on the parameters provided.
        """

        plugin = self.plugin
        family = self.family
        homie = plugin.homie
        childs = homie.childs
        devices = childs.devices
        params = self.params

        _device = params.device


        if _device not in devices:

            raise InvalidParam(
                param='device',
                value=_device,
                error='noexist')


        device = devices[_device]

        _family = device.family

        if _family != family:

            raise InvalidParam(
                param='device',
                value=_device,
                error='invalid')


    @property
    def family(
        self,
    ) -> Literal['philips']:
        """
        Return the value for the attribute from class instance.

        :returns: Value for the attribute from class instance.
        """

        return 'philips'


    @property
    def kinds(
        self,
    ) -> list['HomiePluginKinds']:
        """
        Return the value for the attribute from class instance.

        :returns: Value for the attribute from class instance.
        """

        return ['occur']


    @property
    def params(
        self,
    ) -> 'DriverPhueMotionParams':
        """
        Return the Pydantic model containing the configuration.

        :returns: Pydantic model containing the configuration.
        """

        model = (
            PhueModels
            .drivers()
            .motion())

        params = super().params

        assert isinstance(
            params, model)

        return params


    def occur(  # noqa: CFQ004
        self,
        sitem: 'HomieStreamItem',
    ) -> bool:
        """
        Return the boolean indicating the conditional outcomes.

        :param sitem: Item containing information for operation.
        :returns: Boolean indicating the conditional outcomes.
        """

        plugin = self.plugin
        homie = plugin.homie
        childs = homie.childs
        devices = childs.devices

        params = self.params
        target = params.device
        states = (
            params.states
            or _STATES)


        model = PhueStreamItem

        if not isinstance(sitem, model):
            return NCFalse


        event = sitem.event

        if 'motion' not in event:
            return False


        source = (
            devices[target]
            .source)

        if source is None:
            return False

        service = event['id']


        sensors = (
            phue_sensors(source))

        if 'motion' not in sensors:
            return NCFalse

        intend = sensors['motion']

        if service != intend:
            return False


        valid = getate(
            event,
            'motion/motion_valid')

        if valid is False:
            return NCFalse


        _state = getate(
            event,
            'motion/motion')

        if _state is not None:

            state = 'no_motion'

            if _state is True:
                state = 'motion'

            if state not in states:
                return False


        return _state is not None
