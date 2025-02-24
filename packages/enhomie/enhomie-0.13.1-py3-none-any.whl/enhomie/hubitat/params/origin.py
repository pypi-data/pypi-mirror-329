"""
Functions and routines associated with Enasis Network Homie Automate.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from typing import Annotated
from typing import Any
from typing import Callable
from typing import Optional

from enconnect.hubitat import BridgeParams

from pydantic import Field

from ...homie.params.common import HomieParamsModel



class HubiOriginParams(HomieParamsModel, extra='forbid'):
    """
    Process and validate the Homie configuration parameters.
    """

    bridge: Annotated[
        BridgeParams,
        Field(...,
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

            data['bridge'] = _parse(
                data['bridge'])


        super().__init__(**data)
