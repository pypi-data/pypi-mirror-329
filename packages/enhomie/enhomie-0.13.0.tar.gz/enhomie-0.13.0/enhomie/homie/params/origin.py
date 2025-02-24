"""
Functions and routines associated with Enasis Network Homie Automate.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from typing import Annotated
from typing import Any
from typing import Callable
from typing import Optional

from pydantic import Field

from .child import HomieChildParams
from ...hubitat.params import HubiOriginParams
from ...philips.params import PhueOriginParams
from ...ubiquiti.params import UbiqOriginParams



class HomieOriginParams(HomieChildParams, extra='forbid'):
    """
    Process and validate the Homie configuration parameters.
    """

    hubitat: Annotated[
        Optional[HubiOriginParams],
        Field(None,
              description='Connection specific parameters')]

    philips: Annotated[
        Optional[PhueOriginParams],
        Field(None,
              description='Connection specific parameters')]

    ubiquiti: Annotated[
        Optional[UbiqOriginParams],
        Field(None,
              description='Connection specific parameters')]


    def __init__(
        # NOCVR
        self,
        /,
        _parse: Optional[Callable[..., Any]] = None,
        **data: Any,
    ) -> None:
        """
        Initialize instance for class using provided parameters.
        """


        if _parse is not None:

            parsable = [
                'hubitat',
                'philips',
                'ubiquiti']

            for key in parsable:

                if not data.get(key):
                    continue

                item = data[key]

                item['_parse'] = _parse


        super().__init__(**data)
