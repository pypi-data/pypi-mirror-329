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

from ..homie.params.common import HomieParamsModel



class RestfulServiceParams(HomieParamsModel, extra='forbid'):
    """
    Process and validate the Homie configuration parameters.
    """

    bind_addr: Annotated[
        str,
        Field('127.0.0.1',
              description='Which local address to bind',
              min_length=1)]

    bind_port: Annotated[
        int,
        Field(8420,
              description='Which port on address to bind',
              ge=0, le=65535)]

    authenticate: Annotated[
        Optional[dict[str, str]],
        Field(None,
              description='Credentials for authentication',
              min_length=1)]

    ssl_capem: Annotated[
        Optional[str],
        Field(None,
              description='Filesystem path to certificate',
              min_length=1)]

    ssl_mypem: Annotated[
        Optional[str],
        Field(None,
              description='Filesystem path to certificate',
              min_length=1)]

    ssl_mykey: Annotated[
        Optional[str],
        Field(None,
              description='Filesystem path to certificate',
              min_length=1)]


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
                'bind_addr',
                'bind_port',
                'authentiate',
                'ssl_capem',
                'ssl_mypem',
                'ssl_mykey']

            for key in parsable:

                value = data.get(key)

                if value is None:
                    continue

                value = _parse(value)

                data[key] = value


        super().__init__(**data)
