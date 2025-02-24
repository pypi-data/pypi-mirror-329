"""
Functions and routines associated with Enasis Network Homie Automate.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from typing import Literal
from typing import TYPE_CHECKING

from encommon.times import Time

from .helpers import ubiq_latest
from ..models import UbiqModels
from ...homie.plugins import HomieDriver
from ...utils import InvalidParam

if TYPE_CHECKING:
    from ..params import DriverUbiqClientParams
    from ...homie.plugins import HomiePluginKinds



class DriverUbiqClient(HomieDriver):
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

        _clients = params.clients


        for name in _clients:

            if name in devices:
                continue

            raise InvalidParam(
                param='clients',
                value=name,
                error='noexist')


        for name in _clients:

            device = devices[name]

            _family = device.family

            if _family == family:
                continue

            raise InvalidParam(
                param='clients',
                value=name,
                error='invalid')


    @property
    def family(
        self,
    ) -> Literal['ubiquiti']:
        """
        Return the value for the attribute from class instance.

        :returns: Value for the attribute from class instance.
        """

        return 'ubiquiti'


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
    ) -> 'DriverUbiqClientParams':
        """
        Return the Pydantic model containing the configuration.

        :returns: Pydantic model containing the configuration.
        """

        model = (
            UbiqModels
            .drivers()
            .client())

        params = super().params

        assert isinstance(
            params, model)

        return params


    def where(
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
        targets = params.clients
        since = params.since

        wheres: list[bool] = []


        for target in targets:

            source = (
                devices[target]
                .source)

            if source is None:
                continue

            value = ubiq_latest(source)

            _since = time - value

            wheres.append(
                _since >= since)


        if len(wheres) >= 1:
            return any(wheres)

        return True
