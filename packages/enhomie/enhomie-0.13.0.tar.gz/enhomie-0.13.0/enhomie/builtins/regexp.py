"""
Functions and routines associated with Enasis Network Homie Automate.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from contextlib import suppress
from re import compile
from typing import Literal
from typing import TYPE_CHECKING

from encommon.utils import rgxp_match

from .models import BltnModels
from ..homie.plugins import HomieDriver
from ..utils import InvalidParam

if TYPE_CHECKING:
    from .params import DriverBltnRegexpParams
    from ..homie.plugins import HomiePluginKinds
    from ..homie.threads import HomieStreamItem



class DriverBltnRegexp(HomieDriver):
    """
    Match specific conditions for determining desired state.
    """


    def validate(
        self,
    ) -> None:
        """
        Perform advanced validation on the parameters provided.
        """

        params = self.params

        _rgxps = params.patterns


        for pattern in _rgxps:

            with suppress(Exception):
                compile(pattern)
                continue

            raise InvalidParam(
                param='patterns',
                value=pattern,
                error='invalid')


    @property
    def family(
        self,
    ) -> Literal['builtins']:
        """
        Return the value for the attribute from class instance.

        :returns: Value for the attribute from class instance.
        """

        return 'builtins'


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
    ) -> 'DriverBltnRegexpParams':
        """
        Return the Pydantic model containing the configuration.

        :returns: Pydantic model containing the configuration.
        """

        model = (
            BltnModels
            .drivers()
            .regexp())

        params = super().params

        assert isinstance(
            params, model)

        return params


    def occur(
        self,
        sitem: 'HomieStreamItem',
    ) -> bool:
        """
        Return the boolean indicating the conditional outcomes.

        :param sitem: Item containing information for operation.
        :returns: Boolean indicating the conditional outcomes.
        """

        params = self.params
        patterns = params.patterns
        complete = params.complete

        return rgxp_match(
            values=str(sitem.event),
            patterns=patterns,
            complete=complete)
