"""
Functions and routines associated with Enasis Network Homie Automate.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from typing import Literal
from typing import Optional
from typing import TYPE_CHECKING

from encommon.types import DictStrAny

from .child import HomieChild
from ..models import HomieModels
from ...utils import InvalidParam
from ...utils import MultipleSource

if TYPE_CHECKING:
    from .origin import HomieOrigin
    from ..params import HomieDeviceParams



class HomieDevice(HomieChild):
    """
    Normalize the desired parameters with multiple products.
    """


    def validate(
        self,
    ) -> None:
        """
        Perform advanced validation on the parameters provided.
        """

        homie = self.homie
        childs = homie.childs
        origins = childs.origins

        params = self.params

        _origin = params.origin
        _label = params.label
        _unique = params.unique


        if _origin not in origins:

            raise InvalidParam(
                child=self,
                param='origin',
                value=_origin,
                error='noexist')


        if (_unique is None
                and _label is None):

            raise InvalidParam(
                child=self,
                param='label',
                error='missing')


    @property
    def kind(
        self,
    ) -> Literal['device']:
        """
        Return the value for the attribute from class instance.

        :returns: Value for the attribute from class instance.
        """

        return 'device'


    @property
    def origin(
        self,
    ) -> 'HomieOrigin':
        """
        Return the value for the attribute from class instance.

        :returns: Value for the attribute from class instance.
        """

        homie = self.homie
        childs = homie.childs
        origins = childs.origins

        params = self.params
        origin = params.origin

        return origins[origin]


    @property
    def params(
        self,
    ) -> 'HomieDeviceParams':
        """
        Return the Pydantic model containing the configuration.

        :returns: Pydantic model containing the configuration.
        """

        model = (
            HomieModels
            .device())

        params = super().params

        assert isinstance(
            params, model)

        return params


    @property
    def source(
        self,
    ) -> Optional[DictStrAny]:
        """
        Return the content related to the item in parent system.

        :returns: Content related to the item in parent system.
        """

        homie = self.homie
        childs = homie.childs
        origins = childs.origins

        params = self.params

        _origin = params.origin
        _label = params.label
        _unique = params.unique

        origin = origins[_origin]

        try:

            return origin.source(
                kind='device',
                label=_label,
                unique=_unique)

        except MultipleSource:

            reason = (
                'multiple items '
                'match in source')

            homie.logger.log_e(
                base=self,
                name=self,
                status='multiple',
                reason=reason)

            return None


    @property
    def dumped(
        self,
    ) -> DictStrAny:
        """
        Return the facts about the attributes from the instance.

        :returns: Facts about the attributes from the instance.
        """

        dumped = super().dumped

        origin = self.origin

        present = bool(self.source)

        return dumped | {
            'origin': origin.name,
            'present': present}
