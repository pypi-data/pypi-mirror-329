"""
Functions and routines associated with Enasis Network Homie Automate.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from re import compile
from typing import Annotated
from typing import Any
from typing import Literal
from typing import Optional

from pydantic import Field

from ...homie.params.common import HomieParamsModel



_WEEKDAY = Literal[
    'Monday',
    'Tuesday',
    'Wednesday',
    'Thursday',
    'Friday',
    'Saturday',
    'Sunday']

_TIMERGXP = compile(
    r'^([01]\d|2[0-3])'
    r':([0-5]\d)$')



class DriverBltnPeriodParams(HomieParamsModel, extra='forbid'):
    """
    Process and validate the Homie configuration parameters.
    """

    start: Annotated[
        Optional[str],
        Field(None,
              description='Start time in 24 hour format',
              pattern=_TIMERGXP)]

    stop: Annotated[
        Optional[str],
        Field(None,
              description='Stop time in 24 hour format',
              pattern=_TIMERGXP)]

    days: Annotated[
        Optional[list[_WEEKDAY]],
        Field(None,
              description='Days of the week in scope',
              min_length=1)]

    tzname: Annotated[
        str,
        Field('UTC',
              description='Timezone parsed with Time',
              min_length=1)]


    def __init__(
        # NOCVR
        self,
        /,
        **data: Any,
    ) -> None:
        """
        Initialize instance for class using provided parameters.
        """

        days = data.get('days')

        if isinstance(days, str):
            data['days'] = [days]

        super().__init__(**data)
