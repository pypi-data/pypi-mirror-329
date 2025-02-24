"""
Functions and routines associated with Enasis Network Homie Automate.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from typing import Annotated
from typing import Optional

from pydantic import Field

from .common import HomieParamsModel
from ..common import HomieState



class HomieStageParams(HomieParamsModel, extra='forbid'):
    """
    Process and validate the Homie configuration parameters.
    """

    state: Annotated[
        Optional[HomieState],
        Field(None,
              description='Setting for the light state')]

    color: Annotated[
        Optional[str],
        Field(None,
              description='Setting for the light color',
              min_length=6,
              max_length=6)]

    level: Annotated[
        Optional[int],
        Field(None,
              description='Setting for the light level',
              ge=0, le=100)]
