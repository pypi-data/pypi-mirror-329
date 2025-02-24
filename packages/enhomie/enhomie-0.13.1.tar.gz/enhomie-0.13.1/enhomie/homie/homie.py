"""
Functions and routines associated with Enasis Network Homie Automate.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from copy import deepcopy
from typing import Any
from typing import Optional
from typing import TYPE_CHECKING

from encommon.types import DictStrAny
from encommon.types import NCNone
from encommon.types import clsname
from encommon.types import sort_dict
from encommon.utils import array_ansi
from encommon.utils import print_ansi

from .addons import HomieAspired
from .addons import HomieDesired
from .addons import HomieJinja2
from .addons import HomieLogger
from .addons import HomiePersist
from .childs import HomieChilds
from .models import HomieModels

if TYPE_CHECKING:
    from .common import HomiePrint
    from .common import HomieState
    from .childs import HomieDevice
    from .childs import HomieGroup
    from .childs import HomieScene
    from .config import HomieConfig
    from .params import HomieParams
    from .threads import HomieActionBase
    from .threads import HomieActionNode



class Homie:
    """
    Interact with supported devices to ensure desired state.

    :param config: Primary class instance for configuration.
    """

    __config: 'HomieConfig'

    __logger: HomieLogger
    __jinja2: HomieJinja2
    __persist: HomiePersist

    __childs: HomieChilds

    __desired: HomieDesired
    __aspired: HomieAspired


    def __init__(
        self,
        config: 'HomieConfig',
    ) -> None:
        """
        Initialize instance for class using provided parameters.
        """

        config.logger.log_d(
            base=clsname(self),
            status='initial')

        self.__config = config

        self.__logger = (
            HomieLogger(self))

        self.__jinja2 = (
            HomieJinja2(self))

        self.__persist = (
            HomiePersist(self))

        self.__childs = (
            HomieChilds(self))

        self.childs.validate()

        self.__desired = (
            HomieDesired(self))

        self.__aspired = (
            HomieAspired(self))

        config.logger.log_d(
            base=clsname(self),
            status='created')


    @property
    def config(
        self,
    ) -> 'HomieConfig':
        """
        Return the Config instance containing the configuration.

        :returns: Config instance containing the configuration.
        """

        return self.__config


    @property
    def logger(
        self,
    ) -> HomieLogger:
        """
        Return the value for the attribute from class instance.

        :returns: Value for the attribute from class instance.
        """

        return self.__logger


    @property
    def jinja2(
        self,
    ) -> HomieJinja2:
        """
        Return the value for the attribute from class instance.

        :returns: Value for the attribute from class instance.
        """

        return self.__jinja2


    @property
    def persist(
        self,
    ) -> HomiePersist:
        """
        Return the value for the attribute from class instance.

        :returns: Value for the attribute from class instance.
        """

        return self.__persist


    @property
    def childs(
        self,
    ) -> HomieChilds:
        """
        Return the value for the attribute from class instance.

        :returns: Value for the attribute from class instance.
        """

        return self.__childs


    @property
    def params(
        self,
    ) -> 'HomieParams':
        """
        Return the Pydantic model containing the configuration.

        :returns: Pydantic model containing the configuration.
        """

        return self.config.params


    @property
    def dryrun(
        self,
    ) -> bool:
        """
        Return the value for the attribute from class instance.

        :returns: Value for the attribute from class instance.
        """

        return self.params.dryrun


    @property
    def potent(
        self,
    ) -> bool:
        """
        Return the value for the attribute from class instance.

        :returns: Value for the attribute from class instance.
        """

        return self.params.potent


    @property
    def desired(
        self,
    ) -> HomieDesired:
        """
        Return the related actions matching the provided event.

        :returns: Related actions matching the provided event.
        """

        return self.__desired


    @property
    def aspired(
        self,
    ) -> HomieAspired:
        """
        Return the related desired state for the desired groups.

        :returns: Related desired state for the desired groups.
        """

        return self.__aspired


    def refresh(
        self,
        timeout: Optional[int] = None,
    ) -> bool:
        """
        Refresh the cached information for the remote upstream.

        :param timeout: Timeout waiting for the server response.
        :returns: Boolean indicating the success of the refresh.
        """

        childs = self.childs

        refresh: set[bool] = set()

        origins = (
            childs.origins
            .values())


        for origin in origins:

            result = (
                origin
                .refresh(timeout))

            refresh.add(result)


        return all(refresh)


    @property
    def dumped(
        self,
    ) -> DictStrAny:
        """
        Return the facts about the attributes from the instance.

        :returns: Facts about the attributes from the instance.
        """

        params = deepcopy(
            self.params.endumped)

        childs = deepcopy(
            self.childs.dumped)

        items = childs.items()

        for key, value in items:
            params[key] = value

        return params


    def printer(  # noqa: CFQ001,CFQ004
        self,
        source: 'HomiePrint',
        color: int = 6,
    ) -> None:
        """
        Print the contents for the object within Homie instance.

        :param source: Content which will be shown after header.
        :param color: Override the color used for box character.
        """

        params = self.params
        printer = params.printer

        paction = printer.action
        pupdate = printer.update
        pstream = printer.stream
        pdesire = printer.desire
        paspire = printer.aspire


        HomieActionItem = (
            HomieModels
            .action())

        HomieUpdateItem = (
            HomieModels
            .update())

        HomieStreamItem = (
            HomieModels
            .stream())

        HomieDesiredItem = (
            HomieModels
            .desired())

        HomieAspiredItem = (
            HomieModels
            .aspired())


        action = isinstance(
            source, HomieActionItem)

        if action and not paction:
            return NCNone


        update = isinstance(
            source, HomieUpdateItem)

        if update and not pupdate:
            return NCNone


        stream = isinstance(
            source, HomieStreamItem)

        if stream and not pstream:
            return NCNone


        desired = isinstance(
            source, HomieDesiredItem)

        if desired is True:

            if pdesire is False:
                return NCNone

            source = dict(
                source.__dict__)

            _target = source['target']
            _desire = source['desire']
            _scene = source['scene']

            target = (
                _target.name
                if _target is not None
                else None)

            desire = (
                _desire.name
                if _desire is not None
                else None)

            scene = (
                _scene.name
                if _scene is not None
                else None)

            source |= {
                'target': target,
                'desire': desire,
                'scene': scene}


        aspired = isinstance(
            source, HomieAspiredItem)

        if aspired is True:

            if paspire is False:
                return NCNone

            source = dict(
                source.__dict__)

            _target = source['target']
            _aspire = source['aspire']
            _scene = source['scene']

            target = (
                _target.name
                if _target is not None
                else None)

            aspire = (
                _aspire.name
                if _aspire is not None
                else None)

            scene = (
                _scene.name
                if _scene is not None
                else None)

            source |= {
                'target': target,
                'aspire': aspire,
                'scene': scene}


        line: str = '━'

        print_ansi(
            f'\n<c9{color}>┍'
            f'{line * 63}<c0>')

        dumped = array_ansi(
            source, indent=2)

        print(  # noqa: T201
            f'\n{dumped}')

        print_ansi(
            f'\n<c9{color}>┕'
            f'{line * 63}<c0>\n')


    def get_actions(  # noqa: CFQ002
        self,
        target: 'HomieActionNode',
        *,
        state: Optional['HomieState'] = None,
        color: Optional[str] = None,
        level: Optional[int] = None,
        scene: Optional['HomieScene'] = None,
        force: bool = False,
        change: bool = True,
    ) -> 'HomieActionBase':
        """
        Insert the new item containing information for operation.

        :param target: Device or group settings will be updated.
        :param state: Determine the state related to the target.
        :param color: Determine the color related to the target.
        :param level: Determine the level related to the target.
        :param scene: Determine the scene related to the target.
        :param force: Override the default for full idempotency.
        :param change: Determine whether the change is executed.
        """

        childs = self.childs
        devices = childs.devices

        aitems: 'HomieActionBase' = {}

        something = any([
            state is not None,
            color is not None,
            level is not None,
            scene is not None])

        if something is False:
            return aitems


        def _add_group(
            target: 'HomieGroup',
        ) -> None:

            origin = target.origin

            assert origin is not None

            aitem = (
                origin.get_action(
                    target=target,
                    state=state,
                    color=color,
                    level=level,
                    scene=scene))

            aitems[target] = aitem


        def _add_devices(
            target: 'HomieGroup',
        ) -> None:

            params = target.params
            names = params.devices

            assert names is not None

            for name in names:

                device = devices[name]

                _add_device(device)


        def _add_device(
            target: 'HomieDevice',
        ) -> None:

            origin = target.origin

            aitem = (
                origin.get_action(
                    target=target,
                    state=state,
                    color=color,
                    level=level,
                    scene=scene))

            aitems[target] = aitem


        if target.kind == 'group':

            params = target.params

            if params.devices:
                _add_devices(target)

            if target.origin:
                _add_group(target)


        if target.kind == 'device':
            _add_device(target)


        return sort_dict(aitems)


    def set_actions(
        self,
        aitems: 'HomieActionBase',
        force: bool = False,
        change: bool = True,
    ) -> bool:
        """
        Insert the new item containing information for operation.

        :param aitems: Constructed action objects for operation.
        :param force: Override the default for full idempotency.
        :param change: Determine whether the change is executed.
        :returns: Boolean indicating whether or not was changed.
        """

        changed: set[bool] = set()

        items = aitems.items()

        for target, aitem in items:

            assert target.origin

            origin = target.origin

            result = (
                origin.set_action(
                    target=target,
                    aitem=aitem,
                    force=force,
                    change=change))

            changed.add(result)

        return any(changed)


    def j2parse(
        self,
        value: Any,  # noqa: ANN401
        statics: Optional[DictStrAny] = None,
        literal: bool = True,
    ) -> Any:  # noqa: ANN401
        """
        Return the provided input using the Jinja2 environment.

        :param value: Input that will be processed and returned.
        :param statics: Additional values available for parsing.
        :param literal: Determine if Python objects are evaled.
        :returns: Provided input using the Jinja2 environment.
        """

        return self.__jinja2.parse(
            value, statics, literal)
