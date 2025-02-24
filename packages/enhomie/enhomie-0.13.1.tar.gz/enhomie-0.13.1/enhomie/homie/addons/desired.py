"""
Functions and routines associated with Enasis Network Homie Automate.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from dataclasses import dataclass
from typing import Optional
from typing import TYPE_CHECKING

from encommon.times import Time

if TYPE_CHECKING:
    from ..childs import HomieDesire
    from ..childs import HomieScene
    from ..common import HomieState
    from ..homie import Homie
    from ..threads import HomieActionNode



@dataclass
class HomieDesiredItem:
    """
    Contain information related to the desired child state.
    """

    target: 'HomieActionNode'
    weight: int

    desire: 'HomieDesire'

    state: Optional['HomieState'] = None
    color: Optional[str] = None
    level: Optional[int] = None
    scene: Optional['HomieScene'] = None


    def __init__(
        self,
        target: 'HomieActionNode',
        desire: 'HomieDesire',
    ) -> None:
        """
        Initialize instance for class using provided parameters.

        .. note::
           Somewhat similar to same method in HomieAspiredItem.
        """

        homie = desire.homie
        childs = homie.childs

        params = desire.params
        weight = params.weight

        self.target = target
        self.weight = weight

        self.desire = desire

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
        other: 'HomieDesiredItem',
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


    @property
    def paused(
        self,
    ) -> bool:
        """
        Return the boolean indicating whether operation delayed.

        :returns: Boolean indicating whether operation delayed.
        """

        target = self.target
        desire = self.desire

        return desire.paused(target)


    @property
    def applied(
        self,
    ) -> bool:
        """
        Return the boolean indicating that there will be change.

        :returns: Boolean indicating that there will be change.
        """

        desire = self.desire
        homie = desire.homie
        potent = homie.potent

        target = self.target
        state = self.state
        color = self.color
        level = self.level
        scene = self.scene

        aitems = (
            homie.get_actions(
                target=target,
                state=state,
                color=color,
                level=level,
                scene=scene))

        return not (
            homie.set_actions(
                aitems=aitems,
                force=potent,
                change=False))


    def matched(
        self,
    ) -> None:
        """
        Perform operations when this desire is the most desired.
        """

        target = self.target
        desire = self.desire

        return desire.matched(target)


    def omitted(
        self,
    ) -> None:
        """
        Perform operations when this desire is the most desired.
        """

        target = self.target
        desire = self.desire

        return desire.omitted(target)



_DESIRED = list[HomieDesiredItem]
_STAGING = dict['HomieActionNode', set['HomieDesire']]
_MATCHED = set['HomieDesire']
_TARGETS = dict['HomieActionNode', 'HomieDesiredItem']



class HomieDesired:
    """
    Contain information related to the desired child state.

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


    def items(  # noqa: CFQ001
        self,
        time: Time,
    ) -> _DESIRED:
        """
        Return the action state objects for the related targets.

        ..note::
          Somewhat similar to same method within HomieAspire.

        :param time: Time that will be used in the conditionals.
        :returns: Action state objects for the related targets.
        """

        homie = self.__homie
        persist = homie.persist
        childs = homie.childs

        desires = (
            childs.desires
            .values())

        desired: _DESIRED = []
        prepare: _STAGING = {}
        matched: _MATCHED = set()
        targets: _TARGETS = {}

        model = HomieDesiredItem


        for desire in desires:

            when = desire.when(time)

            if when is False:
                desire.omitted()
                continue

            matched.add(desire)


            devices = desire.devices

            for device in devices:

                if not prepare.get(device):
                    prepare[device] = set()

                (prepare[device]
                 .add(desire))


            groups = desire.groups

            for group in groups:

                if not prepare.get(group):
                    prepare[group] = set()

                (prepare[group]
                 .add(desire))


        items = prepare.items()

        for target, serised in items:

            _serised = sorted(
                serised,
                key=lambda x: x.weight,
                reverse=True)


            for desire in _serised[1:]:

                object = model(
                    target, desire)

                object.omitted()


            desire = _serised[0]

            object = model(
                target, desire)


            if object.applied:

                object.omitted()

                homie.logger.log_d(
                    base=self,
                    item=desire,
                    name=desire,
                    target=target.name,
                    status='omit')

                continue

            if object.paused:

                homie.logger.log_d(
                    base=self,
                    item=desire,
                    name=desire,
                    target=target.name,
                    status='pause')

                continue

            homie.logger.log_d(
                base=self,
                item=desire,
                name=desire,
                target=target.name,
                status='match')

            object.matched()

            targets[target] = object


        for desire in matched:

            store = (
                desire.params
                .store)

            if store is None:
                continue

            if homie.dryrun:
                continue

            statics = {
                'desire': desire}

            for value in store:
                persist.insert(
                    **value.endumped,
                    statics=statics)


        objects = targets.values()

        for object in objects:

            desired.append(object)


        return sorted(desired)
