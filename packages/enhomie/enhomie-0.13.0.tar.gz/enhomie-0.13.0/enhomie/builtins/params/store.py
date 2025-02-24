"""
Functions and routines associated with Enasis Network Homie Automate.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from typing import Annotated
from typing import Literal
from typing import Optional

from pydantic import Field

from ..store import BltnStoreOperas
from ...homie.addons import HomiePersistValue
from ...homie.params.common import HomieParamsModel



class DriverBltnStoreParams(HomieParamsModel, extra='forbid'):
    """
    Process and validate the Homie configuration parameters.
    """

    unique: Annotated[
        str,
        Field(...,
              description='Unique key for the value',
              min_length=1)]

    operator: Annotated[
        Literal[BltnStoreOperas],
        Field(...,
              description='Operator for the condition')]

    value: Annotated[
        Optional[HomiePersistValue],
        Field(None,
              description='Value for the condition')]
