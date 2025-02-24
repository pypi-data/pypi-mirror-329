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
from .occur import HomieOccurParams
from .stage import HomieStageParams
from .store import HomieStoreParams
from .where import HomieWhereParams



class HomieAspireParams(HomieChildParams, extra='forbid'):
    """
    Process and validate the Homie configuration parameters.
    """

    devices: Annotated[
        Optional[list[str]],
        Field(None,
              description='Devices that are in scope',
              min_length=1)]

    groups: Annotated[
        Optional[list[str]],
        Field(None,
              description='Groups that are in scope',
              min_length=1)]

    stage: Annotated[
        Optional[HomieStageParams],
        Field(None,
              description='Default device scene config')]

    scene: Annotated[
        Optional[str],
        Field(None,
              description='Update the group light scene',
              min_length=1)]

    store: Annotated[
        Optional[list[HomieStoreParams]],
        Field(None,
              description='Update values in database',
              min_length=1)]

    occurs: Annotated[
        Optional[list[HomieOccurParams]],
        Field(None,
              description='Plugins for the conditions',
              min_length=1)]

    wheres: Annotated[
        Optional[list[HomieWhereParams]],
        Field(None,
              description='Plugins for the conditions',
              min_length=1)]

    pause: Annotated[
        int,
        Field(3,
              description='Delay before acting again',
              ge=1, le=86400)]


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
        groups = data.get('groups')

        if isinstance(devices, str):
            data['devices'] = [devices]

        if isinstance(groups, str):
            data['groups'] = [groups]

        super().__init__(**data)
