"""
Functions and routines associated with Enasis Network Homie Automate.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from copy import deepcopy
from threading import current_thread
from typing import Any
from typing import Literal
from typing import Optional
from typing import TYPE_CHECKING
from typing import Union

from encommon.colors import Color
from encommon.times import Time
from encommon.types import DictStrAny

from enconnect.philips import Bridge

from .helpers import PhueFetch
from .helpers import PhueMerge
from .helpers import merge_fetch
from .helpers import merge_find
from .helpers import request_action
from .models import PhueModels
from .surgeon import surgeon
from ..homie.childs import HomieOrigin
from ..utils import Idempotent
from ..utils import MultipleSource

if TYPE_CHECKING:
    from ..homie.childs import HomieScene
    from ..homie.common import HomieKinds
    from ..homie.common import HomieState
    from ..homie.threads import HomieActionNode
    from ..homie.threads import HomieActionItem
    from ..homie.threads import HomieStreamItem
    from ..homie.threads import HomieUpdateBase
    from ..homie.threads import HomieUpdateItem



class PhueOrigin(HomieOrigin):
    """
    Contain the relevant attributes from the related source.
    """

    __bridge: Bridge

    __fetch: Optional[PhueFetch]
    __merge: Optional[PhueMerge]


    def __init__(
        self,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        """
        Initialize instance for class using provided parameters.
        """

        super().__init__(
            *args, **kwargs)


        params = (
            self.params
            .philips)

        assert params is not None

        bridge = Bridge(
            params.bridge)


        self.__bridge = bridge

        self.__fetch = None
        self.__merge = None


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
    def bridge(
        self,
    ) -> Bridge:
        """
        Return the value for the attribute from class instance.

        :returns: Value for the attribute from class instance.
        """

        return self.__bridge


    @property
    def fetch(
        self,
    ) -> Optional[PhueFetch]:
        """
        Return the content related to the item in parent system.

        :returns: Content related to the item in parent system.
        """

        fetch = self.__fetch

        return deepcopy(fetch)


    @property
    def merge(
        self,
    ) -> Optional[PhueMerge]:
        """
        Return the content related to the item in parent system.

        :returns: Content related to the item in parent system.
        """

        fetch = self.__fetch
        merge = self.__merge

        if merge is not None:
            return deepcopy(merge)

        if fetch is None:
            return None

        merge = (
            merge_fetch(fetch))

        self.__merge = merge

        return deepcopy(merge)


    def refresh(
        self,
        timeout: Optional[int] = None,
    ) -> bool:
        """
        Refresh the cached information for the remote upstream.

        :param timeout: Timeout waiting for the server response.
        :returns: Boolean indicating the success of the refresh.
        """

        homie = self.homie
        bridge = self.__bridge
        request = bridge.request

        runtime = Time()

        try:

            response = request(
                'get', 'resource',
                timeout=timeout)

            (response
             .raise_for_status())


            fetch = response.json()

            assert isinstance(
                fetch, dict)


            self.__fetch = fetch
            self.__merge = None


            homie.logger.log_d(
                base=self,
                name=self,
                item='refresh',
                elapsed=runtime,
                status='success')

            return True


        except Exception as reason:

            homie.logger.log_e(
                base=self,
                name=self,
                item='refresh',
                elapsed=runtime,
                status='exception',
                exc_info=reason)

            return False


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

        .. note::
           This method is identical to same with other origins.

        :param target: Device or group settings will be updated.
        :param state: Determine the state related to the target.
        :param color: Determine the color related to the target.
        :param level: Determine the level related to the target.
        :param scene: Determine the scene related to the target.
        :returns: New item containing information for operation.
        """

        homie = self.homie
        childs = homie.childs
        scenes = childs.scenes

        model = (
            PhueModels
            .action())

        if isinstance(color, str):
            color = Color(color)

        if isinstance(scene, str):
            scene = scenes[scene]

        return model(
            self, target,
            state=state,
            color=color,
            level=level,
            scene=scene)


    def set_action(  # noqa: CFQ004
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

        homie = self.homie
        childs = homie.childs
        scenes = childs.scenes

        runtime = Time()

        thread = current_thread()


        name = aitem.scene

        scene = (
            scenes[name]
            if name is not None
            else None)


        try:

            request_action(
                self, target,
                state=aitem.state,
                color=aitem.color,
                level=aitem.level,
                scene=scene,
                force=force,
                change=change,
                timeout=timeout)


        except Idempotent:

            if change is False:
                return False

            homie.logger.log_d(
                base=self,
                name=self,
                item='action',
                target=target.name,
                thread=thread.name,
                elapsed=runtime,
                status='nochange')

            return False


        except Exception as reason:

            homie.logger.log_e(
                base=self,
                name=self,
                item='action',
                target=target.name,
                thread=thread.name,
                elapsed=runtime,
                status='exception',
                exc_info=reason)

            return False

        else:

            if change is False:
                return True

            homie.logger.log_d(
                base=self,
                name=self,
                item='action',
                target=target.name,
                thread=thread.name,
                elapsed=runtime,
                status='success')

            return True


    def get_update(
        self,
    ) -> 'HomieUpdateItem':
        """
        Return the new item containing information for operation.

        :returns: New item containing information for operation.
        """

        model = (
            PhueModels
            .update())

        fetch = self.fetch

        assert fetch is not None

        return model(
            self, fetch)


    def set_update(
        self,
        uitem: 'HomieUpdateBase',
    ) -> bool:
        """
        Replace or update internal configuration with provided.

        :param uitem: Item containing information for operation.
        :returns: Boolean indicating whether or not was changed.
        """

        _name = uitem.origin

        assert _name == self.name

        changed = 0


        if hasattr(uitem, 'fetch'):

            fetch = deepcopy(
                uitem.fetch)

            self.__fetch = fetch
            self.__merge = None

            changed += 1


        if hasattr(uitem, 'event'):

            fetch = self.__fetch
            event = uitem.event

            assert fetch is not None

            event = deepcopy(
                uitem.event)

            if surgeon(fetch, event):
                self.__merge = None
                changed += 1


        return changed >= 1


    def get_stream(
        self,
        event: DictStrAny,
    ) -> 'HomieStreamItem':
        """
        Return the new item containing information for operation.

        :param event: Event from the stream for creating object.
        :returns: New item containing information for operation.
        """

        model = (
            PhueModels
            .stream())

        return model(
            self, event)


    def source(
        self,
        kind: Optional['HomieKinds'] = None,
        unique: Optional[str] = None,
        label: Optional[str] = None,
        relate: Optional['HomieActionNode'] = None,
    ) -> Optional[DictStrAny]:
        """
        Return the content related to the item in parent system.

        .. note::
           This method is redundant with other origin classes.

        :param kind: Which kind of Homie object will be located.
        :param unique: Unique identifier within parents system.
        :param label: Friendly name or label within the parent.
        :param relate: Child class instance for Homie Automate.
        :returns: Content related to the item in parent system.
        """

        merge = self.__merge

        if merge is None:
            merge = self.merge

        if merge is None:
            return None

        found = merge_find(
            merge=merge,
            kind=kind,
            unique=unique,
            label=label,
            relate=relate)

        if len(found) == 0:
            return None

        if len(found) == 1:
            return deepcopy(found[0])

        raise MultipleSource
