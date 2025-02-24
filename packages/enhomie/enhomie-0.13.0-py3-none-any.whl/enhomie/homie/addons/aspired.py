"""
Functions and routines associated with Enasis Network Homie Automate.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from dataclasses import dataclass
from typing import Optional
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..childs import HomieAspire
    from ..childs import HomieScene
    from ..common import HomieState
    from ..homie import Homie
    from ..threads import HomieActionNode
    from ..threads import HomieStreamItem



@dataclass
class HomieAspiredItem:
    """
    Contain information related to the aspired child state.
    """

    target: 'HomieActionNode'

    aspire: 'HomieAspire'

    state: Optional['HomieState'] = None
    color: Optional[str] = None
    level: Optional[int] = None
    scene: Optional['HomieScene'] = None


    def __init__(
        self,
        target: 'HomieActionNode',
        aspire: 'HomieAspire',
    ) -> None:
        """
        Initialize instance for class using provided parameters.

        .. note::
           Somewhat similar to same method in HomieDesiredItem.
        """

        homie = aspire.homie
        childs = homie.childs

        params = aspire.params

        self.target = target

        self.aspire = aspire

        scene = params.scene
        stage = params.stage

        self.state = None
        self.color = None
        self.level = None
        self.scene = None


        if scene is not None:

            _scene = (
                childs.scenes
                [scene])

            self.scene = _scene


        if stage is not None:

            _state = stage.state
            _color = stage.color
            _level = stage.level

            self.state = _state
            self.color = _color
            self.level = _level


    def __lt__(
        self,
        other: 'HomieAspiredItem',
    ) -> bool:
        """
        Built-in method for comparing this instance with another.

        .. note::
           Useful with sorting to influence consistent output.

        :param other: Other value being compared with instance.
        :returns: Boolean indicating outcome from the operation.
        """

        name = self.target.name
        _name = other.target.name

        return bool(name < _name)



_ASPIRED = list[HomieAspiredItem]
_MATCHED = set['HomieAspire']



class HomieAspired:
    """
    Contain information related to the aspired child state.

    :param homie: Primary class instance for Homie Automate.
    """

    __homie: 'Homie'


    def __init__(
        self,
        homie: 'Homie',
    ) -> None:
        """
        Initialize instance for class using provided parameters.
        """

        self.__homie = homie


    def items(
        self,
        sitem: 'HomieStreamItem',
    ) -> _ASPIRED:
        """
        Return the action state objects for the related targets.

        ..note::
          Somewhat similar to same method within HomieDesire.

        :param sitem: Item containing information for operation.
        :returns: Action state objects for the related targets.
        """

        homie = self.__homie
        persist = homie.persist
        childs = homie.childs

        aspires = (
            childs.aspires
            .values())

        aspired: _ASPIRED = []
        matched: _MATCHED = set()

        model = HomieAspiredItem


        for aspire in aspires:

            when = aspire.when(sitem)

            if when is False:
                continue

            matched.add(aspire)

            if aspire.paused:

                homie.logger.log_d(
                    base=self,
                    item=aspire,
                    name=aspire,
                    status='pause')

                continue

            homie.logger.log_d(
                base=self,
                item=aspire,
                name=aspire,
                status='match')

            aspire.matched()


        for aspire in matched:

            store = (
                aspire.params
                .store)

            if store is None:
                continue

            if homie.dryrun:
                continue

            statics = {
                'aspire': aspire}

            for value in store:
                persist.insert(
                    **value.endumped,
                    statics=statics)


        for aspire in matched:

            devices = aspire.devices

            for device in devices:

                object = model(
                    device, aspire)

                aspired.append(object)

            groups = aspire.groups

            for group in groups:

                object = model(
                    group, aspire)

                aspired.append(object)


        return list(aspired)
