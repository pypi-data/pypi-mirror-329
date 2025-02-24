"""
Functions and routines associated with Enasis Network Homie Automate.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from typing import Literal
from typing import TYPE_CHECKING

from encommon.times import Time

from .models import BltnModels
from ..homie.plugins import HomieDriver
from ..utils import InvalidParam
from ..utils import UnexpectedCondition

if TYPE_CHECKING:
    from .params import DriverBltnStoreParams
    from ..homie.plugins import HomiePluginKinds



BltnStoreOperas = Literal[
    'present',
    'absent',
    'eq', 'neq',
    'lt', 'lte',
    'gt', 'gte']

_SINGLES = ['present', 'absent']



class DriverBltnStore(HomieDriver):
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

        _opera = params.operator
        _value = params.value


        if (_opera in _SINGLES
                and _value is not None):

            raise InvalidParam(
                param='operator',
                value=_value,
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
    ) -> 'DriverBltnStoreParams':
        """
        Return the Pydantic model containing the configuration.

        :returns: Pydantic model containing the configuration.
        """

        model = (
            BltnModels
            .drivers()
            .store())

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

        params = self.params
        unique = params.unique
        opera = params.operator
        value = params.value


        store = (
            homie.persist
            .select(unique))


        if opera == 'present':
            return store is not None

        if opera == 'absent':
            return store is None


        if (isinstance(value, int | float)
                and store is not None
                and store is not False
                and store is not True):

            store = float(store)

            if opera == 'lt':
                return store < value

            if opera == 'lte':
                return store <= value

            if opera == 'gt':
                return store > value

            if opera == 'gte':
                return store >= value


        if opera == 'neq':
            return store != value

        if opera == 'eq':
            return store == value


        raise UnexpectedCondition
