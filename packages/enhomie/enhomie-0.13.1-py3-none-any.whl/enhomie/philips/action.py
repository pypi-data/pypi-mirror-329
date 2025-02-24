"""
Functions and routines associated with Enasis Network Homie Automate.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from dataclasses import dataclass
from typing import Any
from typing import Optional

from ..homie.threads import HomieAction
from ..homie.threads import HomieActionItem
from ..homie.threads import HomieActionNode



@dataclass
class PhueActionItem(HomieActionItem):
    """
    Contain information for sharing using the Python queue.
    """


    def __init__(
        self,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        """
        Initialize instance for class using provided parameters.
        """

        super().__init__(
            *args, **kwargs)



class PhueAction(HomieAction):
    """
    Common methods and routines for Homie Automate threads.
    """


    def execute(
        self,
        aitem: HomieActionItem,
    ) -> None:
        """
        Perform the operation related to Homie service threads.

        :param aitem: Item containing information for operation.
        """

        assert isinstance(
            aitem, PhueActionItem)

        homie = self.homie
        childs = homie.childs
        devices = childs.devices
        groups = childs.groups

        params = homie.params
        potent = homie.potent

        timeout = (
            params.service
            .timeout.action)

        _device = aitem.device
        _group = aitem.group


        target: Optional[
            HomieActionNode]

        target = None

        if _device is not None:
            target = devices[_device]

        elif _group is not None:
            target = groups[_group]

        if target is None:

            homie.logger.log_e(
                base=self,
                item=aitem,
                status='notarget')

            return None


        origin = target.origin

        if origin is None:

            homie.logger.log_e(
                base=self,
                item=target,
                name=target,
                status='absent')

            return None

        origin.set_action(
            target=target,
            aitem=aitem,
            force=potent,
            timeout=timeout)
