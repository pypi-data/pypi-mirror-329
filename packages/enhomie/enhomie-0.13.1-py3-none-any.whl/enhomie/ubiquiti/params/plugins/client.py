"""
Functions and routines associated with Enasis Network Homie Automate.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from typing import Annotated
from typing import Any

from pydantic import Field

from ....homie.params.common import HomieParamsModel



class DriverUbiqClientParams(HomieParamsModel, extra='forbid'):
    """
    Process and validate the Homie configuration parameters.
    """

    clients: Annotated[
        list[str],
        Field(...,
              description='Clients that are in scope',
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

        clients = data.get('clients')

        if isinstance(clients, str):
            data['clients'] = [clients]

        super().__init__(**data)
