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

from ..models import PhueModels
from ..stream import PhueStreamItem
from ...homie.plugins import HomieDriver
from ...utils import InvalidParam

if TYPE_CHECKING:
    from ..params import DriverPhueSceneParams
    from ...homie.plugins import HomiePluginKinds
    from ...homie.threads import HomieStreamItem



PhueSceneState = Literal[
    'active',
    'inactive']

_STATES = list(
    get_args(PhueSceneState))



class DriverPhueScene(HomieDriver):
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
        homie = plugin.homie
        childs = homie.childs
        groups = childs.groups
        scenes = childs.scenes
        params = self.params

        _scene = params.scene
        _group = params.group


        if _scene not in scenes:

            raise InvalidParam(
                param='scene',
                value=_scene,
                error='noexist')


        if _group not in groups:

            raise InvalidParam(
                param='group',
                value=_group,
                error='noexist')


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
    ) -> 'DriverPhueSceneParams':
        """
        Return the Pydantic model containing the configuration.

        :returns: Pydantic model containing the configuration.
        """

        model = (
            PhueModels
            .drivers()
            .scene())

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
        scenes = childs.scenes
        groups = childs.groups

        params = self.params
        _scene = params.scene
        _group = params.group
        states = (
            params.states
            or _STATES)

        scene = scenes[_scene]
        group = groups[_group]


        model = PhueStreamItem

        if not isinstance(sitem, model):
            return NCFalse


        event = sitem.event

        type = event.get('type')

        if type != 'scene':
            return False


        origin = group.origin

        if origin is None:
            return False

        source = scene.source(
            origin, group)

        if source is None:
            return False

        service = event['id']


        intend = source['id']

        if service != intend:
            return False


        _state = getate(
            event, 'status/active')

        if _state is None:
            return NCFalse

        if _state != 'inactive':
            _state = 'active'


        return _state in states
