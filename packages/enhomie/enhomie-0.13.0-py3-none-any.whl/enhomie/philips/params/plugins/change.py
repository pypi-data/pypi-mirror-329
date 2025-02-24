"""
Functions and routines associated with Enasis Network Homie Automate.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from typing import Annotated
from typing import Any
from typing import Optional

from pydantic import Field

from ...plugins.change import PhueChangeSensor
from ....homie.params.common import HomieParamsModel



class DriverPhueChangeParams(HomieParamsModel, extra='forbid'):
    """
    Process and validate the Homie configuration parameters.
    """

    devices: Annotated[
        list[str],
        Field(...,
              description='Devices that are in scope',
              min_length=1)]

    sensors: Annotated[
        Optional[list[PhueChangeSensor]],
        Field(None,
              description='Sensors that will be matched',
              min_length=1)]

    since: Annotated[
        int,
        Field(0,
              description='Minimum time since changed',
              ge=0)]


    def __init__(
        # NOCVR
        self,
        /,
        **data: Any,
    ) -> None:
        """
        Initialize instance for class using provided parameters.
        """

        devices = data.get('devices')
        sensors = data.get('sensors')

        if isinstance(devices, str):
            data['devices'] = [devices]

        if isinstance(sensors, str):
            data['sensors'] = [sensors]

        super().__init__(**data)
