"""
Functions and routines associated with Enasis Network Homie Automate.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from copy import deepcopy
from typing import Any
from typing import Literal
from typing import Optional
from typing import TYPE_CHECKING

from encommon.times import Time
from encommon.types import DictStrAny

from enconnect.ubiquiti import Router

from .helpers import UbiqFetch
from .helpers import UbiqMerge
from .helpers import merge_fetch
from .helpers import merge_find
from .models import UbiqModels
from ..homie.childs import HomieOrigin
from ..utils import MultipleSource

if TYPE_CHECKING:
    from ..homie.common import HomieKinds
    from ..homie.threads import HomieActionNode
    from ..homie.threads import HomieUpdateItem
    from ..homie.threads import HomieUpdateBase



class UbiqOrigin(HomieOrigin):
    """
    Contain the relevant attributes from the related source.
    """

    __router: Router

    __fetch: Optional[UbiqFetch]
    __merge: Optional[UbiqMerge]


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
            .ubiquiti)

        assert params is not None

        router = Router(
            params.router)


        self.__router = router

        self.__fetch = None
        self.__merge = None


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
    def router(
        self,
    ) -> Router:
        """
        Return the value for the attribute from class instance.

        :returns: Value for the attribute from class instance.
        """

        return self.__router


    @property
    def fetch(
        self,
    ) -> Optional[UbiqFetch]:
        """
        Return the content related to the item in parent system.

        :returns: Content related to the item in parent system.
        """

        fetch = self.__fetch

        return deepcopy(fetch)


    @property
    def merge(
        self,
    ) -> Optional[UbiqMerge]:
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
        router = self.__router
        request = router.reqroxy

        runtime = Time()

        try:

            response1 = request(
                'get', 'rest/user',
                timeout=timeout)

            (response1
             .raise_for_status())

            response2 = request(
                'get', 'stat/sta',
                timeout=timeout)

            (response2
             .raise_for_status())


            fetch1 = response1.json()
            fetch2 = response2.json()

            assert isinstance(
                fetch1, dict)

            assert isinstance(
                fetch2, dict)

            fetch = {
                'historic': fetch1,
                'realtime': fetch2}


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


    def get_update(
        self,
    ) -> 'HomieUpdateItem':
        """
        Return the new item containing information for operation.

        :returns: New item containing information for operation.
        """

        model = (
            UbiqModels
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


        assert hasattr(
            uitem, 'fetch')


        fetch = deepcopy(
            uitem.fetch)

        self.__fetch = fetch
        self.__merge = None

        return True


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

        assert relate is None

        found = merge_find(
            merge=merge,
            kind=kind,
            unique=unique,
            label=label)

        if len(found) == 0:
            return None

        if len(found) == 1:
            return deepcopy(found[0])

        raise MultipleSource
