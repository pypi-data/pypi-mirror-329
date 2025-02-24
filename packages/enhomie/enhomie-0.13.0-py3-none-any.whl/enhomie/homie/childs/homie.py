"""
Functions and routines associated with Enasis Network Homie Automate.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from copy import deepcopy
from typing import TYPE_CHECKING
from typing import Type

from encommon.types import DictStrAny
from encommon.utils import fuzz_match

from .aspire import HomieAspire
from .desire import HomieDesire
from .device import HomieDevice
from .group import HomieGroup
from .origin import HomieOrigin
from .scene import HomieScene
from ...utils import InvalidChild

if TYPE_CHECKING:
    from ..homie import Homie



HomieOrigins = dict[str, HomieOrigin]
HomieDevices = dict[str, HomieDevice]

HomieGroups = dict[str, HomieGroup]
HomieScenes = dict[str, HomieScene]

HomieAspires = dict[str, HomieAspire]
HomieDesires = dict[str, HomieDesire]



class HomieChilds:
    """
    Contain the object instances for related Homie children.

    :param homie: Primary class instance for Homie Automate.
    """

    __homie: 'Homie'

    __origins: HomieOrigins
    __devices: HomieDevices

    __groups: HomieGroups
    __scenes: HomieScenes

    __desires: HomieDesires
    __aspires: HomieAspires


    def __init__(
        self,
        homie: 'Homie',
    ) -> None:
        """
        Initialize instance for class using provided parameters.
        """

        homie.logger.log_d(
            base=self,
            status='initial')

        self.__homie = homie

        self.__origins = {}
        self.__devices = {}

        self.__groups = {}
        self.__scenes = {}

        self.__desires = {}
        self.__aspires = {}

        self.build_objects()

        homie.logger.log_i(
            base=self,
            status='created')


    def build_objects(
        self,
    ) -> None:
        """
        Construct instances using the configuration parameters.
        """

        self.__build_origins()
        self.__build_devices()

        self.__build_groups()
        self.__build_scenes()

        self.__build_desires()
        self.__build_aspires()


    def __build_origins(
        self,
    ) -> None:
        """
        Construct instances using the configuration parameters.
        """

        homie = self.__homie
        params = homie.params
        origins = params.origins

        if origins is None:
            return None


        childs: HomieOrigins = {}


        items = origins.items()

        for name, origin in items:

            child = (
                self.
                get_origin(name))

            childs[name] = child(
                homie, name, origin)


        self.__origins = childs


    def __build_devices(
        self,
    ) -> None:
        """
        Construct instances using the configuration parameters.
        """

        homie = self.__homie
        params = homie.params
        devices = params.devices

        if devices is None:
            return None


        childs: HomieDevices = {}


        items = devices.items()

        for name, device in items:

            child = (
                self
                .get_device(name))

            childs[name] = child(
                homie, name, device)


        self.__devices = childs


    def __build_groups(
        self,
    ) -> None:
        """
        Construct instances using the configuration parameters.
        """

        homie = self.__homie
        params = homie.params
        groups = params.groups

        if groups is None:
            return None

        model = HomieGroup


        childs: HomieGroups = {}


        items = groups.items()

        for name, group in items:

            object = model(
                homie, name, group)

            childs[name] = object


        self.__groups = childs


    def __build_scenes(
        self,
    ) -> None:
        """
        Construct instances using the configuration parameters.
        """

        homie = self.__homie
        params = homie.params
        scenes = params.scenes

        if scenes is None:
            return None

        model = HomieScene


        childs: HomieScenes = {}


        items = scenes.items()

        for name, scene in items:

            object = model(
                homie, name, scene)

            childs[name] = object


        self.__scenes = childs


    def __build_desires(
        self,
    ) -> None:
        """
        Construct instances using the configuration parameters.
        """

        homie = self.__homie
        params = homie.params
        desires = params.desires

        if desires is None:
            return None

        model = HomieDesire


        filters = params.filters
        filter = filters.desires


        def _filter() -> bool:

            if filter is None:
                return False

            matched = (
                fuzz_match(name, filter))

            return not matched


        childs: HomieDesires = {}


        items = desires.items()

        for name, desire in items:

            if _filter() is True:
                continue

            object = model(
                homie, name, desire)

            childs[name] = object


        self.__desires = childs


    def __build_aspires(
        self,
    ) -> None:
        """
        Construct instances using the configuration parameters.
        """

        homie = self.__homie
        params = homie.params
        aspires = params.aspires

        if aspires is None:
            return None

        model = HomieAspire


        filters = params.filters
        filter = filters.aspires


        def _filter() -> bool:

            if filter is None:
                return False

            matched = (
                fuzz_match(name, filter))

            return not matched


        childs: HomieAspires = {}


        items = aspires.items()

        for name, aspire in items:

            if _filter() is True:
                continue

            object = model(
                homie, name, aspire)

            childs[name] = object


        self.__aspires = childs


    def validate(
        self,
    ) -> None:
        """
        Perform advanced validation on the parameters provided.
        """


        origins = (
            self.__origins
            .values())

        for origin in origins:
            origin.validate()


        devices = (
            self.__devices
            .values())

        for device in devices:
            device.validate()


        groups = (
            self.__groups
            .values())

        for group in groups:
            group.validate()


        scenes = (
            self.__scenes
            .values())

        for scene in scenes:
            scene.validate()


        desires = (
            self.__desires
            .values())

        for desire in desires:
            desire.validate()


        aspires = (
            self.__aspires
            .values())

        for aspire in aspires:
            aspire.validate()


    @property
    def origins(
        self,
    ) -> HomieOrigins:
        """
        Return the value for the attribute from class instance.

        :returns: Value for the attribute from class instance.
        """

        origins = self.__origins

        return dict(origins)


    @property
    def devices(
        self,
    ) -> HomieDevices:
        """
        Return the value for the attribute from class instance.

        :returns: Value for the attribute from class instance.
        """

        devices = self.__devices

        return dict(devices)


    @property
    def groups(
        self,
    ) -> HomieGroups:
        """
        Return the value for the attribute from class instance.

        :returns: Value for the attribute from class instance.
        """

        groups = self.__groups

        return dict(groups)


    @property
    def scenes(
        self,
    ) -> HomieScenes:
        """
        Return the value for the attribute from class instance.

        :returns: Value for the attribute from class instance.
        """

        scenes = self.__scenes

        return dict(scenes)


    @property
    def desires(
        self,
    ) -> HomieDesires:
        """
        Return the value for the attribute from class instance.

        :returns: Value for the attribute from class instance.
        """

        desires = self.__desires

        return dict(desires)


    @property
    def aspires(
        self,
    ) -> HomieAspires:
        """
        Return the value for the attribute from class instance.

        :returns: Value for the attribute from class instance.
        """

        aspires = self.__aspires

        return dict(aspires)


    @property
    def dumped(
        self,
    ) -> DictStrAny:
        """
        Return the facts about the attributes from the instance.

        :returns: Facts about the attributes from the instance.
        """

        origins = self.origins
        devices = self.devices
        groups = self.groups
        scenes = self.scenes
        desires = self.desires
        aspires = self.aspires

        dumped: DictStrAny = {

            'origins': {
                k: v.dumped for k, v
                in origins.items()},

            'devices': {
                k: v.dumped for k, v
                in devices.items()},

            'groups': {
                k: v.dumped for k, v
                in groups.items()},

            'scenes': {
                k: v.dumped for k, v
                in scenes.items()},

            'desires': {
                k: v.dumped for k, v
                in desires.items()},

            'aspires': {
                k: v.dumped for k, v
                in aspires.items()}}

        return deepcopy(dumped)


    def get_origin(
        self,
        name: str,
    ) -> Type['HomieOrigin']:
        """
        Return the Homie class definition for its instantiation.

        :param name: Name of the object within the Homie config.
        :returns: Homie class definition for its instantiation.
        """

        from ...hubitat import HubiOrigin
        from ...philips import PhueOrigin
        from ...ubiquiti import UbiqOrigin


        homie = self.__homie
        params = homie.params
        origins = params.origins

        assert origins is not None

        origin = origins[name]


        _hubitat = origin.hubitat
        _philips = origin.philips
        _ubiquiti = origin.ubiquiti

        if _hubitat is not None:
            return HubiOrigin

        if _philips is not None:
            return PhueOrigin

        if _ubiquiti is not None:
            return UbiqOrigin


        raise InvalidChild(
            name, phase='initial')


    def get_device(
        self,
        name: str,
    ) -> Type['HomieDevice']:
        """
        Return the Homie class definition for its instantiation.

        :param name: Name of the object within the Homie config.
        :returns: Homie class definition for its instantiation.
        """

        from ...hubitat import HubiDevice
        from ...philips import PhueDevice
        from ...ubiquiti import UbiqDevice


        homie = self.__homie
        params = homie.params
        origins = self.__origins
        devices = params.devices

        assert devices is not None

        device = devices[name]
        origin = origins[
            device.origin]


        family = origin.family

        if family == 'hubitat':
            return HubiDevice

        if family == 'philips':
            return PhueDevice

        if family == 'ubiquiti':
            return UbiqDevice


        raise InvalidChild(
            name, phase='initial')
