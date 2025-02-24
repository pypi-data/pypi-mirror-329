"""
Functions and routines associated with Enasis Network Homie Automate.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from typing import TYPE_CHECKING
from typing import Type

if TYPE_CHECKING:
    from .common import HomiePluginKinds
    from .driver import HomieDriver
    from ..common import HomieFamily
    from ..homie import Homie
    from ..params import HomiePluginParams



class HomiePlugin:
    """
    Match specific conditions for determining desired state.

    :param homie: Primary class instance for Homie Automate.
    :param params: Parameters used to instantiate the class.
    """

    __homie: 'Homie'

    __params: 'HomiePluginParams'
    __drivers: list['HomieDriver']


    def __init__(
        self,
        homie: 'Homie',
        params: 'HomiePluginParams',
    ) -> None:
        """
        Initialize instance for class using provided parameters.
        """

        self.__homie = homie
        self.__params = params

        self.__drivers = []

        self.__build_drivers()


    def __build_drivers(
        self,
    ) -> None:
        """
        Construct instances using the configuration parameters.
        """

        params = self.params

        objects = self.get_drivers()


        drivers: list['HomieDriver'] = []


        items = (
            params.__dict__
            .items())

        for name, driver in items:

            if name not in objects:
                continue

            if driver is None:
                continue

            _object = objects[name]

            object = (
                _object(self, driver))

            drivers.append(object)


        self.__drivers = drivers


    def validate(
        self,
    ) -> None:
        """
        Perform advanced validation on the parameters provided.
        """

        drivers = self.__drivers

        for driver in drivers:
            driver.validate()


    @property
    def homie(
        self,
    ) -> 'Homie':
        """
        Return the Homie instance to which the instance belongs.

        :returns: Homie instance to which the instance belongs.
        """

        return self.__homie


    @property
    def family(
        self,
    ) -> 'HomieFamily':
        """
        Return the value for the attribute from class instance.

        :returns: Value for the attribute from class instance.
        """

        return 'builtins'


    @property
    def kind(
        self,
    ) -> 'HomiePluginKinds':
        """
        Return the value for the attribute from class instance.

        :returns: Value for the attribute from class instance.
        """

        raise NotImplementedError


    @property
    def params(
        self,
    ) -> 'HomiePluginParams':
        """
        Return the Pydantic model containing the configuration.

        :returns: Pydantic model containing the configuration.
        """

        return self.__params


    @property
    def drivers(
        self,
    ) -> list['HomieDriver']:
        """
        Return the value for the attribute from class instance.

        :returns: Value for the attribute from class instance.
        """

        return list(self.__drivers)


    def get_drivers(
        self,
    ) -> dict[str, Type['HomieDriver']]:
        """
        Return the Homie class definition for its instantiation.

        :returns: Homie class definition for its instantiation.
        """

        raise NotImplementedError
