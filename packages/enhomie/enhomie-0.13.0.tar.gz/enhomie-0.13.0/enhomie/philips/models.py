"""
Functions and routines associated with Enasis Network Homie Automate.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from typing import Any
from typing import Callable
from typing import TYPE_CHECKING
from typing import Type

if TYPE_CHECKING:
    from .action import PhueActionItem
    from .params import DriverPhueButtonParams
    from .params import DriverPhueChangeParams
    from .params import DriverPhueContactParams
    from .params import DriverPhueMotionParams
    from .params import DriverPhueSceneParams
    from .params import PhueOriginParams
    from .update import PhueUpdateItem
    from .stream import PhueStreamItem



class PhueDriverHelpers:
    """
    Return the class object that was imported within method.

    .. note::
       These are used with the Homie Automate Jinja2 parser.
    """


    @classmethod
    def sensors(
        cls,
    ) -> Callable[..., Any]:
        """
        Return the class object that was imported within method.

        :returns: Class object that was imported within method.
        """

        from .plugins import (
            phue_sensors)

        return phue_sensors


    @classmethod
    def changed(
        cls,
    ) -> Callable[..., Any]:
        """
        Return the class object that was imported within method.

        :returns: Class object that was imported within method.
        """

        from .plugins import (
            phue_changed)

        return phue_changed


    @classmethod
    def current(
        cls,
    ) -> Callable[..., Any]:
        """
        Return the class object that was imported within method.

        :returns: Class object that was imported within method.
        """

        from .plugins import (
            phue_current)

        return phue_current



class PhueDriverModels:
    """
    Return the class object that was imported within method.
    """


    @classmethod
    def button(
        cls,
    ) -> Type['DriverPhueButtonParams']:
        """
        Return the class object that was imported within method.

        :returns: Class object that was imported within method.
        """

        from .params import (
            DriverPhueButtonParams)

        return DriverPhueButtonParams


    @classmethod
    def change(
        cls,
    ) -> Type['DriverPhueChangeParams']:
        """
        Return the class object that was imported within method.

        :returns: Class object that was imported within method.
        """

        from .params import (
            DriverPhueChangeParams)

        return DriverPhueChangeParams


    @classmethod
    def contact(
        cls,
    ) -> Type['DriverPhueContactParams']:
        """
        Return the class object that was imported within method.

        :returns: Class object that was imported within method.
        """

        from .params import (
            DriverPhueContactParams)

        return DriverPhueContactParams


    @classmethod
    def motion(
        cls,
    ) -> Type['DriverPhueMotionParams']:
        """
        Return the class object that was imported within method.

        :returns: Class object that was imported within method.
        """

        from .params import (
            DriverPhueMotionParams)

        return DriverPhueMotionParams


    @classmethod
    def scene(
        cls,
    ) -> Type['DriverPhueSceneParams']:
        """
        Return the class object that was imported within method.

        :returns: Class object that was imported within method.
        """

        from .params import (
            DriverPhueSceneParams)

        return DriverPhueSceneParams


    @classmethod
    def helpers(
        cls,
    ) -> Type['PhueDriverHelpers']:
        """
        Return the class object that was imported within method.

        :returns: Class object that was imported within method.
        """

        return PhueDriverHelpers



class PhueModels:
    """
    Return the class object that was imported within method.
    """


    @classmethod
    def origin(
        cls,
    ) -> Type['PhueOriginParams']:
        """
        Return the class object that was imported within method.

        :returns: Class object that was imported within method.
        """

        from .params import (
            PhueOriginParams)

        return PhueOriginParams


    @classmethod
    def action(
        cls,
    ) -> Type['PhueActionItem']:
        """
        Return the class object that was imported within method.

        :returns: Class object that was imported within method.
        """

        from .action import (
            PhueActionItem)

        return PhueActionItem


    @classmethod
    def update(
        cls,
    ) -> Type['PhueUpdateItem']:
        """
        Return the class object that was imported within method.

        :returns: Class object that was imported within method.
        """

        from .update import (
            PhueUpdateItem)

        return PhueUpdateItem


    @classmethod
    def stream(
        cls,
    ) -> Type['PhueStreamItem']:
        """
        Return the class object that was imported within method.

        :returns: Class object that was imported within method.
        """

        from .stream import (
            PhueStreamItem)

        return PhueStreamItem


    @classmethod
    def drivers(
        cls,
    ) -> Type['PhueDriverModels']:
        """
        Return the class object that was imported within method.

        :returns: Class object that was imported within method.
        """

        return PhueDriverModels
