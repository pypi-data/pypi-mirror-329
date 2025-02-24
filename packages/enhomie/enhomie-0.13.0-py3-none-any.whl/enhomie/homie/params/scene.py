"""
Functions and routines associated with Enasis Network Homie Automate.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from typing import Annotated
from typing import Optional

from pydantic import Field

from .child import HomieChildParams
from .stage import HomieStageParams



class HomieSceneParams(HomieChildParams, extra='forbid'):
    """
    Process and validate the Homie configuration parameters.
    """

    label: Annotated[
        Optional[str],
        Field(None,
              description='Scene name in the origin',
              min_length=1)]

    stage: Annotated[
        HomieStageParams,
        Field(default_factory=HomieStageParams,
              description='Default device scene config')]

    devices: Annotated[
        Optional[dict[str, HomieStageParams]],
        Field(None,
              description='Device specific scene config',
              min_length=1)]
