"""
Functions and routines associated with Enasis Network Homie Automate.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from typing import TYPE_CHECKING
from typing import Type

if TYPE_CHECKING:
    from .params import DriverBltnPeriodParams
    from .params import DriverBltnRegexpParams
    from .params import DriverBltnStoreParams



class BltnDriverModels:
    """
    Return the class object that was imported within method.
    """


    @classmethod
    def store(
        cls,
    ) -> Type['DriverBltnStoreParams']:
        """
        Return the class object that was imported within method.

        :returns: Class object that was imported within method.
        """

        from .params import (
            DriverBltnStoreParams)

        return DriverBltnStoreParams


    @classmethod
    def period(
        cls,
    ) -> Type['DriverBltnPeriodParams']:
        """
        Return the class object that was imported within method.

        :returns: Class object that was imported within method.
        """

        from .params import (
            DriverBltnPeriodParams)

        return DriverBltnPeriodParams


    @classmethod
    def regexp(
        cls,
    ) -> Type['DriverBltnRegexpParams']:
        """
        Return the class object that was imported within method.

        :returns: Class object that was imported within method.
        """

        from .params import (
            DriverBltnRegexpParams)

        return DriverBltnRegexpParams



class BltnModels:
    """
    Return the class object that was imported within method.
    """


    @classmethod
    def drivers(
        cls,
    ) -> Type['BltnDriverModels']:
        """
        Return the class object that was imported within method.

        :returns: Class object that was imported within method.
        """

        return BltnDriverModels
