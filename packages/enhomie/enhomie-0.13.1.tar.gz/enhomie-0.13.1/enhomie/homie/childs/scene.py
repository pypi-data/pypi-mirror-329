"""
Functions and routines associated with Enasis Network Homie Automate.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from copy import deepcopy
from typing import Literal
from typing import Optional
from typing import TYPE_CHECKING

from encommon.types import DictStrAny
from encommon.types import merge_dicts

from .child import HomieChild
from ..common import HomieStage
from ..models import HomieModels
from ...utils import InvalidParam
from ...utils import MultipleSource

if TYPE_CHECKING:
    from .origin import HomieOrigin
    from .device import HomieDevice
    from ..threads import HomieActionNode
    from ..params import HomieSceneParams



class HomieScene(HomieChild):
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
        devices = childs.devices

        params = self.params

        _label = params.label
        _stage = params.stage
        _devices = params.devices


        if (_stage is None
                and _label is None):

            raise InvalidParam(
                child=self,
                error='minimal')


        for value in _devices or []:

            if value in devices:
                continue

            raise InvalidParam(
                child=self,
                param='devices',
                value=value,
                error='noexist')


    @property
    def kind(
        self,
    ) -> Literal['scene']:
        """
        Return the value for the attribute from class instance.

        :returns: Value for the attribute from class instance.
        """

        return 'scene'


    @property
    def params(
        self,
    ) -> 'HomieSceneParams':
        """
        Return the Pydantic model containing the configuration.

        :returns: Pydantic model containing the configuration.
        """

        model = (
            HomieModels
            .scene())

        params = super().params

        assert isinstance(
            params, model)

        return params


    def source(
        self,
        origin: 'HomieOrigin',
        relate: Optional['HomieActionNode'] = None,
    ) -> Optional[DictStrAny]:
        """
        Return the content related to the item in parent system.

        :param origin: Child class instance for Homie Automate.
        :param relate: Child class instance for Homie Automate.
        :returns: Content related to the item in parent system.
        """

        homie = self.homie
        params = self.params

        _label = params.label

        try:

            return origin.source(
                kind='scene',
                label=_label,
                relate=relate)

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


    def stage(
        self,
        device: Optional['HomieDevice'] = None,
    ) -> HomieStage:
        """
        Return the configuration for the device or the defaults.

        :param device: Child class instance for Homie Automate.
        :returns: Configuration for the device or the defaults.
        """

        params = self.params
        stage = params.stage
        devices = params.devices

        pruned = (
            stage
            .enpruned)

        pruned = deepcopy(pruned)


        def _override() -> None:

            assert device and devices

            config = devices[
                device.name]

            _pruned = (
                config
                .enpruned)

            _pruned = deepcopy(_pruned)

            merge_dicts(
                dict1=pruned,
                dict2=_pruned,
                force=True)


        if device and devices:

            name = device.name

            if name in devices:
                _override()


        return HomieStage(**pruned)
