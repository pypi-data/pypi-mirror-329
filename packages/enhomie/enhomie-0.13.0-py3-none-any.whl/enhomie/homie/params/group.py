"""
Functions and routines associated with Enasis Network Homie Automate.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from typing import Annotated
from typing import Any
from typing import Optional

from pydantic import Field

from .child import HomieChildParams



class HomieGroupParams(HomieChildParams, extra='forbid'):
    """
    Process and validate the Homie configuration parameters.
    """

    origin: Annotated[
        Optional[str],
        Field(None,
              description='Origin where group exists',
              min_length=1)]

    label: Annotated[
        Optional[str],
        Field(None,
              description='Group name in the origin',
              min_length=1)]

    devices: Annotated[
        Optional[list[str]],
        Field(None,
              description='List of devices in group',
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

        devices = data.get('devices')

        if isinstance(devices, str):
            data['devices'] = [devices]

        super().__init__(**data)
