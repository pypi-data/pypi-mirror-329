"""
Functions and routines associated with Enasis Network Homie Automate.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from typing import Literal
from typing import Optional
from typing import TYPE_CHECKING
from typing import Union

from encommon.colors import Color
from encommon.types import DictStrAny

from .child import HomieChild
from ..addons import HomieQueue
from ..models import HomieModels
from ...utils import InvalidParam

if TYPE_CHECKING:
    from .scene import HomieScene
    from ..common import HomieFamily
    from ..common import HomieKinds
    from ..common import HomieState
    from ..params import HomieOriginParams
    from ..threads import HomieActionItem
    from ..threads import HomieActionNode
    from ..threads import HomieUpdateBase
    from ..threads import HomieUpdateItem
    from ..threads import HomieStreamItem



class HomieOrigin(HomieChild):
    """
    Normalize the desired parameters with multiple products.
    """


    def validate(
        self,
    ) -> None:
        """
        Perform advanced validation on the parameters provided.
        """

        params = self.params

        _hubitat = params.hubitat
        _philips = params.philips
        _ubiquiti = params.ubiquiti


        enabled = [
            1 if _hubitat else 0,
            1 if _philips else 0,
            1 if _ubiquiti else 0]

        if sum(enabled) != 1:

            raise InvalidParam(
                child=self,
                error='minimal')


    @property
    def family(
        self,
    ) -> 'HomieFamily':
        """
        Return the value for the attribute from class instance.

        :returns: Value for the attribute from class instance.
        """

        raise NotImplementedError


    @property
    def kind(
        self,
    ) -> Literal['origin']:
        """
        Return the value for the attribute from class instance.

        :returns: Value for the attribute from class instance.
        """

        return 'origin'


    @property
    def params(
        self,
    ) -> 'HomieOriginParams':
        """
        Return the Pydantic model containing the configuration.

        :returns: Pydantic model containing the configuration.
        """

        model = (
            HomieModels
            .origin())

        params = super().params

        assert isinstance(
            params, model)

        return params


    def refresh(
        self,
        timeout: Optional[int] = None,
    ) -> bool:
        """
        Refresh the cached information for the remote upstream.

        :param timeout: Timeout waiting for the server response.
        :returns: Boolean indicating the success of the refresh.
        """

        raise NotImplementedError


    def source(
        self,
        kind: Optional['HomieKinds'] = None,
        unique: Optional[str] = None,
        label: Optional[str] = None,
        relate: Optional['HomieActionNode'] = None,
    ) -> Optional[DictStrAny]:
        """
        Return the content related to the item in parent system.

        :param kind: Which kind of Homie object will be located.
        :param unique: Unique identifier within parents system.
        :param label: Friendly name or label within the parent.
        :param relate: Child class instance for Homie Automate.
        :returns: Content related to the item in parent system.
        """

        raise NotImplementedError


    @property
    def dumped(
        self,
    ) -> DictStrAny:
        """
        Return the facts about the attributes from the instance.

        :returns: Facts about the attributes from the instance.
        """

        dumped = super().dumped

        present = bool(self.source)

        return dumped | {
            'present': present}


    def get_action(
        self,
        target: 'HomieActionNode',
        *,
        state: Optional['HomieState'] = None,
        color: Optional[str | Color] = None,
        level: Optional[int] = None,
        scene: Optional[Union[str, 'HomieScene']] = None,
    ) -> 'HomieActionItem':
        """
        Return the new item containing information for operation.

        :param target: Device or group settings will be updated.
        :param state: Determine the state related to the target.
        :param color: Determine the color related to the target.
        :param level: Determine the level related to the target.
        :param scene: Determine the scene related to the target.
        :returns: New item containing information for operation.
        """

        raise NotImplementedError


    def set_action(
        self,
        target: 'HomieActionNode',
        aitem: 'HomieActionItem',
        force: bool = False,
        change: bool = True,
        timeout: Optional[int] = None,
    ) -> bool:
        """
        Perform the provided action with specified Homie target.

        :param target: Device or group settings will be updated.
        :param aitem: Item containing information for operation.
        :param force: Override the default for full idempotency.
        :param change: Determine whether the change is executed.
        :param timeout: Timeout waiting for the server response.
        :returns: Boolean indicating whether or not was changed.
        """

        raise NotImplementedError


    def put_action(  # noqa: CFQ002
        self,
        aqueue: HomieQueue['HomieActionItem'],
        target: 'HomieActionNode',
        *,
        state: Optional['HomieState'] = None,
        color: Optional[str | Color] = None,
        level: Optional[int] = None,
        scene: Optional[Union[str, 'HomieScene']] = None,
    ) -> None:
        """
        Insert the new item containing information for operation.

        :param aqueue: Queue instance where the item is received.
        :param target: Device or group settings will be updated.
        :param state: Determine the state related to the target.
        :param color: Determine the color related to the target.
        :param level: Determine the level related to the target.
        :param scene: Determine the scene related to the target.
        """

        aitem = (
            self.get_action(
                target=target,
                state=state,
                color=color,
                level=level,
                scene=scene))

        aqueue.put(aitem)


    def get_update(
        self,
    ) -> 'HomieUpdateItem':
        """
        Return the new item containing information for operation.

        :returns: New item containing information for operation.
        """

        raise NotImplementedError


    def set_update(
        self,
        uitem: 'HomieUpdateBase',
    ) -> bool:
        """
        Replace or update internal configuration with provided.

        :param uitem: Item containing information for operation.
        :returns: Boolean indicating whether or not was changed.
        """

        raise NotImplementedError


    def put_update(
        self,
        uqueue: HomieQueue['HomieUpdateItem'],
    ) -> None:
        """
        Insert the new item containing information for operation.

        :param uqueue: Queue instance where the item is received.
        """

        uitem = self.get_update()

        uqueue.put(uitem)


    def get_stream(
        self,
        event: DictStrAny,
    ) -> 'HomieStreamItem':
        """
        Return the new item containing information for operation.

        :param event: Event from the stream for creating object.
        :returns: New item containing information for operation.
        """

        raise NotImplementedError


    def put_stream(
        self,
        squeue: HomieQueue['HomieStreamItem'],
        event: DictStrAny,
    ) -> None:
        """
        Insert the new item containing information for operation.

        :param squeue: Queue instance where the item is received.
        :param event: Event from the stream for creating object.
        """

        stream = (
            self
            .get_stream(event))

        squeue.put(stream)
