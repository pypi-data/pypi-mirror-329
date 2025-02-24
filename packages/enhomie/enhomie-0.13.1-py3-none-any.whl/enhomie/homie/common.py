"""
Functions and routines associated with Enasis Network Homie Automate.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from dataclasses import dataclass
from typing import Literal
from typing import Optional
from typing import TYPE_CHECKING
from typing import Union

from encommon.colors import Color
from encommon.utils.stdout import ANSIARRAY

if TYPE_CHECKING:
    from .threads import HomieThreadItem
    from .addons import HomieAspiredItem
    from .addons import HomieDesiredItem



HomieFamily = Literal[
    'builtins',
    'hubitat',
    'philips',
    'ubiquiti']

HomieKinds = Literal[
    'origin',
    'device',
    'group',
    'scene',
    'aspire',
    'desire']

HomieState = Literal[
    'poweron',
    'nopower']

HomiePrint = Union[
    ANSIARRAY,
    'HomieThreadItem',
    'HomieDesiredItem',
    'HomieAspiredItem']



@dataclass
class HomieStage:
    """
    Contain information about the parameters for the scene.
    """

    state: Optional[HomieState] = None
    color: Optional[Color] = None
    level: Optional[int] = None


    def __init__(
        self,
        state: Optional[HomieState] = None,
        color: Optional[str | Color] = None,
        level: Optional[int] = None,
    ) -> None:
        """
        Initialize instance for class using provided parameters.
        """

        if isinstance(color, str):
            color = Color(color)

        self.state = state
        self.color = color
        self.level = level
