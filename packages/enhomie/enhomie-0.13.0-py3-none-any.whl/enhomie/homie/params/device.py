"""
Functions and routines associated with Enasis Network Homie Automate.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from typing import Annotated
from typing import Optional

from pydantic import Field

from .child import HomieChildParams



class HomieDeviceParams(HomieChildParams, extra='forbid'):
    """
    Process and validate the Homie configuration parameters.
    """

    origin: Annotated[
        str,
        Field(...,
              description='Origin where device exists',
              min_length=1)]

    label: Annotated[
        Optional[str],
        Field(None,
              description='Device name in the origin',
              min_length=1)]

    unique: Annotated[
        Optional[str],
        Field(None,
              description='Unique identifier in origin',
              min_length=1)]
