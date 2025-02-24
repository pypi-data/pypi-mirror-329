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
    from ..params import DriverPhueButtonParams
    from ...homie.plugins import HomiePluginKinds
    from ...homie.threads import HomieStreamItem



PhueButtonEvent = Literal[
    'initial_press',
    'long_release',
    'short_release']

PhueButtonSensor = Literal[
    'button1',
    'button2',
    'button3',
    'button4']

_EVENTS = list(
    get_args(PhueButtonEvent))

_SENSORS = list(
    get_args(PhueButtonSensor))



class DriverPhueButton(HomieDriver):
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
    ) -> 'DriverPhueButtonParams':
        """
        Return the Pydantic model containing the configuration.

        :returns: Pydantic model containing the configuration.
        """

        model = (
            PhueModels
            .drivers()
            .button())

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
        sensor = params.sensor
        events = (
            params.events
            or _EVENTS)


        model = PhueStreamItem

        if not isinstance(sitem, model):
            return NCFalse


        event = sitem.event

        if 'button' not in event:
            return False


        source = (
            devices[target]
            .source)

        if source is None:
            return False

        service = event['id']


        sensors = (
            phue_sensors(source))

        if sensor not in sensors:
            return NCFalse

        intend = sensors[sensor]

        if service != intend:
            return False


        _event = getate(
            event,
            'button/last_event')

        if _event not in events:
            return False


        return True
