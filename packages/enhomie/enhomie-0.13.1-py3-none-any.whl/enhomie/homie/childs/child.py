"""
Functions and routines associated with Enasis Network Homie Automate.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from typing import TYPE_CHECKING

from encommon.types import DictStrAny

if TYPE_CHECKING:
    from ..common import HomieFamily
    from ..common import HomieKinds
    from ..homie import Homie
    from ..params import HomieChildParams



class HomieChild:
    """
    Normalize the desired parameters with multiple products.

    :param homie: Primary class instance for Homie Automate.
    :param name: Name of the object within the Homie config.
    :param params: Parameters used to instantiate the class.
    """

    __homie: 'Homie'

    __name: str
    __params: 'HomieChildParams'


    def __init__(
        self,
        homie: 'Homie',
        name: str,
        params: 'HomieChildParams',
    ) -> None:
        """
        Initialize instance for class using provided parameters.
        """

        homie.logger.log_d(
            base=self,
            name=name,
            status='initial')

        self.__homie = homie
        self.__name = name
        self.__params = params

        self.__post__()

        homie.logger.log_d(
            base=self,
            name=name,
            status='created')


    def __post__(
        self,
    ) -> None:
        """
        Initialize instance for class using provided parameters.
        """


    def validate(
        self,
    ) -> None:
        """
        Perform advanced validation on the parameters provided.
        """

        raise NotImplementedError


    def __lt__(
        self,
        other: 'HomieChild',
    ) -> bool:
        """
        Built-in method for comparing this instance with another.

        .. note::
           Useful with sorting to influence consistent output.

        :param other: Other value being compared with instance.
        :returns: Boolean indicating outcome from the operation.
        """

        name = self.name
        _name = other.name

        return name < _name


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
    def name(
        self,
    ) -> str:
        """
        Return the value for the attribute from class instance.

        :returns: Value for the attribute from class instance.
        """

        return self.__name


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
    ) -> 'HomieKinds':
        """
        Return the value for the attribute from class instance.

        :returns: Value for the attribute from class instance.
        """

        raise NotImplementedError


    @property
    def params(
        self,
    ) -> 'HomieChildParams':
        """
        Return the Pydantic model containing the configuration.

        :returns: Pydantic model containing the configuration.
        """

        return self.__params


    @property
    def dumped(
        self,
    ) -> DictStrAny:
        """
        Return the facts about the attributes from the instance.

        :returns: Facts about the attributes from the instance.
        """

        params = self.__params
        dumped = params.endumped

        return {
            'name': self.name,
            'family': self.family,
            'kind': self.kind,
            'params': dumped}
