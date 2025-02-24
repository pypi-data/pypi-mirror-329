"""
Functions and routines associated with Enasis Network Homie Automate.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from typing import Annotated
from typing import Any
from typing import Optional

from pydantic import Field

from ...plugins.button import PhueButtonEvent
from ...plugins.button import PhueButtonSensor
from ....homie.params.common import HomieParamsModel



class DriverPhueButtonParams(HomieParamsModel, extra='forbid'):
    """
    Process and validate the Homie configuration parameters.
    """

    device: Annotated[
        str,
        Field(...,
              description='Device that is in scope',
              min_length=1)]

    events: Annotated[
        Optional[list[PhueButtonEvent]],
        Field(None,
              description='Events that will be matched',
              min_length=1)]

    sensor: Annotated[
        PhueButtonSensor,
        Field(...,
              description='Sensor that will be matched')]


    def __init__(
        # NOCVR
        self,
        /,
        **data: Any,
    ) -> None:
        """
        Initialize instance for class using provided parameters.
        """

        events = data.get('events')

        if isinstance(events, str):
            data['events'] = [events]

        super().__init__(**data)
