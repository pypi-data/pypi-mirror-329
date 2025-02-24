"""
Functions and routines associated with Enasis Network Homie Automate.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from typing import TYPE_CHECKING

from encommon.times import Time

from ..params.common import HomieParamsModel

if TYPE_CHECKING:
    from .common import HomiePluginKinds
    from .plugin import HomiePlugin
    from ..common import HomieFamily
    from ..threads import HomieStreamItem



class HomieDriver:
    """
    Match specific conditions for determining desired state.

    :param plugin: Plugin class instance for Homie Automate.
    :param params: Parameters used to instantiate the class.
    """

    __plugin: 'HomiePlugin'

    __params: HomieParamsModel


    def __init__(
        self,
        plugin: 'HomiePlugin',
        params: HomieParamsModel,
    ) -> None:
        """
        Initialize instance for class using provided parameters.
        """

        self.__plugin = plugin
        self.__params = params

        self.__post__()


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


    @property
    def plugin(
        self,
    ) -> 'HomiePlugin':
        """
        Return the Homie instance to which the instance belongs.

        :returns: Homie instance to which the instance belongs.
        """

        return self.__plugin


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
    def kinds(
        self,
    ) -> list['HomiePluginKinds']:
        """
        Return the value for the attribute from class instance.

        :returns: Value for the attribute from class instance.
        """

        raise NotImplementedError


    @property
    def params(
        self,
    ) -> HomieParamsModel:
        """
        Return the Pydantic model containing the configuration.

        :returns: Pydantic model containing the configuration.
        """

        return self.__params


    def occur(
        self,
        sitem: 'HomieStreamItem',
    ) -> bool:
        """
        Return the boolean indicating the conditional outcomes.

        :param sitem: Item containing information for operation.
        :returns: Boolean indicating the conditional outcomes.
        """

        raise NotImplementedError


    def where(
        self,
        time: Time,
    ) -> bool:
        """
        Return the boolean indicating the conditional outcomes.

        :param time: Time that will be used in the conditionals.
        :returns: Boolean indicating the conditional outcomes.
        """

        raise NotImplementedError
