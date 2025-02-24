"""
Functions and routines associated with Enasis Network Homie Automate.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from dataclasses import dataclass
from typing import Optional
from typing import TYPE_CHECKING
from typing import Union

from encommon.colors import Color

from .thread import HomieThread
from .thread import HomieThreadItem

if TYPE_CHECKING:
    from ..childs import HomieDevice
    from ..childs import HomieGroup
    from ..childs import HomieOrigin
    from ..childs import HomieScene
    from ..common import HomieState



HomieActionBase = dict[
    'HomieActionNode',
    'HomieActionItem']

HomieActionNode = Union[
    'HomieGroup', 'HomieDevice']



@dataclass
class HomieActionItem(HomieThreadItem):
    """
    Contain information for sharing using the Python queue.
    """

    group: Optional[str] = None
    device: Optional[str] = None

    state: Optional['HomieState'] = None
    color: Optional[Color] = None
    level: Optional[int] = None
    scene: Optional[str] = None


    def __init__(  # noqa: CFQ002
        self,
        origin: 'HomieOrigin',
        target: HomieActionNode,
        *,
        state: Optional['HomieState'] = None,
        color: Optional[str | Color] = None,
        level: Optional[int] = None,
        scene: Optional['HomieScene'] = None,
    ) -> None:
        """
        Initialize instance for class using provided parameters.
        """

        if isinstance(color, str):
            color = Color(color)

        name = target.name
        kind = target.kind

        if kind == 'group':
            self.group = name

        if kind == 'device':
            self.device = name

        self.state = state
        self.color = color
        self.level = level
        self.scene = (
            scene.name
            if scene is not None
            else None)

        super().__init__(origin)



class HomieAction(HomieThread):
    """
    Common methods and routines for Homie Automate threads.
    """


    def operate(
        self,
    ) -> None:
        """
        Perform the operation related to Homie service threads.
        """

        # Where actions executed

        homie = self.homie
        childs = homie.childs
        origins = childs.origins
        member = self.member
        vacate = member.vacate
        aqueue = self.aqueue

        origin = self.origin
        name = origin.name

        while not aqueue.empty:

            aitem = aqueue.get()

            if vacate.is_set():
                continue

            if self.expired(aitem):
                continue

            _origin = origins[
                aitem.origin]

            _name = _origin.name
            assert name == _name

            self.execute(aitem)


    def execute(
        self,
        aitem: HomieActionItem,
    ) -> None:
        """
        Perform the operation related to Homie service threads.

        :param aitem: Item containing information for operation.
        """

        raise NotImplementedError
