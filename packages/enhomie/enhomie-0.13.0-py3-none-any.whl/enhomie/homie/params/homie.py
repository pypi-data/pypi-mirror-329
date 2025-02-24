"""
Functions and routines associated with Enasis Network Homie Automate.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from typing import Annotated
from typing import Any
from typing import Callable
from typing import Optional

from encommon.config import Params

from pydantic import Field

from .aspire import HomieAspireParams
from .common import HomieParamsModel
from .desire import HomieDesireParams
from .device import HomieDeviceParams
from .group import HomieGroupParams
from .origin import HomieOriginParams
from .persist import HomiePersistParams
from .scene import HomieSceneParams
from .service import HomieServiceParams
from ...restful import RestfulServiceParams



class HomiePrinterParams(HomieParamsModel, extra='forbid'):
    """
    Process and validate the Homie configuration parameters.
    """

    action: Annotated[
        bool,
        Field(False,
              description='Print the actions to console')]

    update: Annotated[
        bool,
        Field(False,
              description='Print the updates to console')]

    stream: Annotated[
        bool,
        Field(False,
              description='Print the streams to console')]

    desire: Annotated[
        bool,
        Field(False,
              description='Print the aspires to console')]

    aspire: Annotated[
        bool,
        Field(False,
              description='Print the aspires to console')]



class HomieFiltersParams(HomieParamsModel, extra='forbid'):
    """
    Process and validate the Homie configuration parameters.
    """

    aspires: Annotated[
        Optional[list[str]],
        Field(None,
              description='Patterns the names must match',
              min_length=1)]

    desires: Annotated[
        Optional[list[str]],
        Field(None,
              description='Patterns the names must match',
              min_length=1)]



class HomieParams(Params, extra='forbid'):
    """
    Process and validate the core configuration parameters.
    """

    database: Annotated[
        str,
        Field('sqlite:///:memory:',
              description='Database connection string',
              min_length=1)]

    dryrun: Annotated[
        bool,
        Field(False,
              description='Determine if changes applied')]

    potent: Annotated[
        bool,
        Field(True,
              description='Ignore idempotency in change')]

    printer: Annotated[
        HomiePrinterParams,
        Field(default_factory=HomiePrinterParams,
              description='Print the stream to console')]

    service: Annotated[
        HomieServiceParams,
        Field(default_factory=HomieServiceParams,
              description='Parameters for Homie Service')]

    restful: Annotated[
        RestfulServiceParams,
        Field(default_factory=RestfulServiceParams,
              description='Parameters for Homie RESTful')]

    persists: Annotated[
        Optional[dict[str, HomiePersistParams]],
        Field(None,
              description='Parameters for common persists',
              min_length=1)]

    filters: Annotated[
        HomieFiltersParams,
        Field(default_factory=HomieFiltersParams,
              description='Determine object instantiation')]

    origins: Annotated[
        Optional[dict[str, HomieOriginParams]],
        Field(None,
              description='Parameters for Homie origins',
              min_length=1)]

    devices: Annotated[
        Optional[dict[str, HomieDeviceParams]],
        Field(None,
              description='Parameters for Homie devices',
              min_length=1)]

    groups: Annotated[
        Optional[dict[str, HomieGroupParams]],
        Field(None,
              description='Parameters for Homie groups',
              min_length=1)]

    scenes: Annotated[
        Optional[dict[str, HomieSceneParams]],
        Field(None,
              description='Parameters for Homie scenes',
              min_length=1)]

    desires: Annotated[
        Optional[dict[str, HomieDesireParams]],
        Field(None,
              description='Parameters for Homie desires',
              min_length=1)]

    aspires: Annotated[
        Optional[dict[str, HomieAspireParams]],
        Field(None,
              description='Parameters for Homie aspires',
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
                'origins',
                'devices',
                'groups',
                'scenes',
                'desires',
                'aspires']

            for key in parsable:

                if not data.get(key):
                    continue

                values = (
                    data[key]
                    .values())

                for item in values:
                    item['_parse'] = _parse


            parsable = [
                'database',
                'dryrun',
                'potent',
                'printer',
                'service',
                'restful',
                'filters']

            for key in parsable:

                value = data.get(key)

                if value is None:
                    continue

                value = _parse(value)

                data[key] = value


        super().__init__(**data)
