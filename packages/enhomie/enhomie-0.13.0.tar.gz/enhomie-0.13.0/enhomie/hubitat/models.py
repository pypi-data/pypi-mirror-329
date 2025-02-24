"""
Functions and routines associated with Enasis Network Homie Automate.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from typing import TYPE_CHECKING
from typing import Type

if TYPE_CHECKING:
    from .action import HubiActionItem
    from .params import HubiOriginParams
    from .update import HubiUpdateItem



class HubiModels:
    """
    Return the class object that was imported within method.
    """


    @classmethod
    def origin(
        cls,
    ) -> Type['HubiOriginParams']:
        """
        Return the class object that was imported within method.

        :returns: Class object that was imported within method.
        """

        from .params import (
            HubiOriginParams)

        return HubiOriginParams


    @classmethod
    def action(
        cls,
    ) -> Type['HubiActionItem']:
        """
        Return the class object that was imported within method.

        :returns: Class object that was imported within method.
        """

        from .action import (
            HubiActionItem)

        return HubiActionItem


    @classmethod
    def update(
        cls,
    ) -> Type['HubiUpdateItem']:
        """
        Return the class object that was imported within method.

        :returns: Class object that was imported within method.
        """

        from .update import (
            HubiUpdateItem)

        return HubiUpdateItem
