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
class HubiActionItem(HomieActionItem):
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



class HubiAction(HomieAction):
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
            aitem, HubiActionItem)

        homie = self.homie
        childs = homie.childs
        devices = childs.devices

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

        assert _group is None

        if target is None:

            homie.logger.log_e(
                base=self,
                item=aitem,
                status='notarget')

            return None


        origin = target.origin

        assert origin is not None

        origin.set_action(
            target=target,
            aitem=aitem,
            force=potent,
            timeout=timeout)
