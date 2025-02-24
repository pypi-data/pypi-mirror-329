"""
Functions and routines associated with Enasis Network Homie Automate.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from typing import Literal
from typing import TYPE_CHECKING
from typing import get_args

from encommon.times import Time

from .helpers import phue_changed
from ..models import PhueModels
from ...homie.plugins import HomieDriver
from ...utils import InvalidParam

if TYPE_CHECKING:
    from ..params import DriverPhueChangeParams
    from ...homie.plugins import HomiePluginKinds



PhueChangeSensor = Literal[
    'button1',
    'button2',
    'button3',
    'button4',
    'contact',
    'motion',
    'temperature']

_SENSORS = list(
    get_args(PhueChangeSensor))



class DriverPhueChange(HomieDriver):
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

        _devices = params.devices


        for name in _devices:

            if name in devices:
                continue

            raise InvalidParam(
                param='devices',
                value=name,
                error='noexist')


        for name in _devices:

            device = devices[name]

            _family = device.family

            if _family == family:
                continue

            raise InvalidParam(
                param='devices',
                value=name,
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

        return ['where']


    @property
    def params(
        self,
    ) -> 'DriverPhueChangeParams':
        """
        Return the Pydantic model containing the configuration.

        :returns: Pydantic model containing the configuration.
        """

        model = (
            PhueModels
            .drivers()
            .change())

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

        plugin = self.plugin
        homie = plugin.homie
        childs = homie.childs
        devices = childs.devices

        params = self.params
        targets = params.devices
        since = params.since
        sensors = (
            params.sensors
            or _SENSORS)

        wheres: list[bool] = []


        def _process() -> None:

            if key not in sensors:
                return None

            if value is None:
                return None

            _since = time - value

            wheres.append(
                _since >= since)


        for target in targets:

            source = (
                devices[target]
                .source)

            if source is None:
                continue

            items = (
                phue_changed(source)
                .items())

            for key, value in items:
                _process()


        if len(wheres) >= 1:
            return any(wheres)

        return True
