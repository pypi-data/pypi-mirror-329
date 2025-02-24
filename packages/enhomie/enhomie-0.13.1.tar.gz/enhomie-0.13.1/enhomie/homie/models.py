"""
Functions and routines associated with Enasis Network Homie Automate.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from typing import TYPE_CHECKING
from typing import Type

if TYPE_CHECKING:
    from .addons import HomieAspiredItem
    from .addons import HomieDesiredItem
    from .addons import HomieQueueItem
    from .common import HomieStage
    from .params import HomieParams
    from .params import HomiePrinterParams
    from .params import HomieChildParams
    from .params import HomieOriginParams
    from .params import HomieDeviceParams
    from .params import HomieGroupParams
    from .params import HomieSceneParams
    from .params import HomieAspireParams
    from .params import HomieDesireParams
    from .params import HomiePluginParams
    from .params import HomieOccurParams
    from .params import HomieWhereParams
    from .params import HomieServiceParams
    from .threads import HomieActionItem
    from .threads import HomieStreamItem
    from .threads import HomieThreadItem
    from .threads import HomieUpdateItem
    from ..builtins import BltnModels
    from ..hubitat import HubiModels
    from ..philips import PhueModels
    from ..ubiquiti import UbiqModels



class HomieModels:
    """
    Return the class object that was imported within method.
    """


    @classmethod
    def homie(
        cls,
    ) -> Type['HomieParams']:
        """
        Return the class object that was imported within method.

        :returns: Class object that was imported within method.
        """

        from .params import (
            HomieParams)

        return HomieParams


    @classmethod
    def printer(
        cls,
    ) -> Type['HomiePrinterParams']:
        """
        Return the class object that was imported within method.

        :returns: Class object that was imported within method.
        """

        from .params import (
            HomiePrinterParams)

        return HomiePrinterParams


    @classmethod
    def service(
        cls,
    ) -> Type['HomieServiceParams']:
        """
        Return the class object that was imported within method.

        :returns: Class object that was imported within method.
        """

        from .params import (
            HomieServiceParams)

        return HomieServiceParams


    @classmethod
    def builtins(
        cls,
    ) -> Type['BltnModels']:
        """
        Return the class object that was imported within method.

        :returns: Class object that was imported within method.
        """

        from ..builtins import (
            BltnModels)

        return BltnModels


    @classmethod
    def hubitat(
        cls,
    ) -> Type['HubiModels']:
        """
        Return the class object that was imported within method.

        :returns: Class object that was imported within method.
        """

        from ..hubitat import (
            HubiModels)

        return HubiModels


    @classmethod
    def philips(
        cls,
    ) -> Type['PhueModels']:
        """
        Return the class object that was imported within method.

        :returns: Class object that was imported within method.
        """

        from ..philips import (
            PhueModels)

        return PhueModels


    @classmethod
    def ubiquiti(
        cls,
    ) -> Type['UbiqModels']:
        """
        Return the class object that was imported within method.

        :returns: Class object that was imported within method.
        """

        from ..ubiquiti import (
            UbiqModels)

        return UbiqModels


    @classmethod
    def child(
        cls,
    ) -> Type['HomieChildParams']:
        """
        Return the class object that was imported within method.

        :returns: Class object that was imported within method.
        """

        from .params import (
            HomieChildParams)

        return HomieChildParams


    @classmethod
    def origin(
        cls,
    ) -> Type['HomieOriginParams']:
        """
        Return the class object that was imported within method.

        :returns: Class object that was imported within method.
        """

        from .params import (
            HomieOriginParams)

        return HomieOriginParams


    @classmethod
    def device(
        cls,
    ) -> Type['HomieDeviceParams']:
        """
        Return the class object that was imported within method.

        :returns: Class object that was imported within method.
        """

        from .params import (
            HomieDeviceParams)

        return HomieDeviceParams


    @classmethod
    def group(
        cls,
    ) -> Type['HomieGroupParams']:
        """
        Return the class object that was imported within method.

        :returns: Class object that was imported within method.
        """

        from .params import (
            HomieGroupParams)

        return HomieGroupParams


    @classmethod
    def scene(
        cls,
    ) -> Type['HomieSceneParams']:
        """
        Return the class object that was imported within method.

        :returns: Class object that was imported within method.
        """

        from .params import (
            HomieSceneParams)

        return HomieSceneParams


    @classmethod
    def desire(
        cls,
    ) -> Type['HomieDesireParams']:
        """
        Return the class object that was imported within method.

        :returns: Class object that was imported within method.
        """

        from .params import (
            HomieDesireParams)

        return HomieDesireParams


    @classmethod
    def aspire(
        cls,
    ) -> Type['HomieAspireParams']:
        """
        Return the class object that was imported within method.

        :returns: Class object that was imported within method.
        """

        from .params import (
            HomieAspireParams)

        return HomieAspireParams


    @classmethod
    def plugin(
        cls,
    ) -> Type['HomiePluginParams']:
        """
        Return the class object that was imported within method.

        :returns: Class object that was imported within method.
        """

        from .params import (
            HomiePluginParams)

        return HomiePluginParams


    @classmethod
    def occur(
        cls,
    ) -> Type['HomieOccurParams']:
        """
        Return the class object that was imported within method.

        :returns: Class object that was imported within method.
        """

        from .params import (
            HomieOccurParams)

        return HomieOccurParams


    @classmethod
    def where(
        cls,
    ) -> Type['HomieWhereParams']:
        """
        Return the class object that was imported within method.

        :returns: Class object that was imported within method.
        """

        from .params import (
            HomieWhereParams)

        return HomieWhereParams


    @classmethod
    def stage(
        cls,
    ) -> Type['HomieStage']:
        """
        Return the class object that was imported within method.

        :returns: Class object that was imported within method.
        """

        from .common import (
            HomieStage)

        return HomieStage


    @classmethod
    def queue(
        cls,
    ) -> Type['HomieQueueItem']:
        """
        Return the class object that was imported within method.

        :returns: Class object that was imported within method.
        """

        from .addons import (
            HomieQueueItem)

        return HomieQueueItem


    @classmethod
    def thread(
        cls,
    ) -> Type['HomieThreadItem']:
        """
        Return the class object that was imported within method.

        :returns: Class object that was imported within method.
        """

        from .threads import (
            HomieThreadItem)

        return HomieThreadItem


    @classmethod
    def action(
        cls,
    ) -> Type['HomieActionItem']:
        """
        Return the class object that was imported within method.

        :returns: Class object that was imported within method.
        """

        from .threads import (
            HomieActionItem)

        return HomieActionItem


    @classmethod
    def update(
        cls,
    ) -> Type['HomieUpdateItem']:
        """
        Return the class object that was imported within method.

        :returns: Class object that was imported within method.
        """

        from .threads import (
            HomieUpdateItem)

        return HomieUpdateItem


    @classmethod
    def stream(
        cls,
    ) -> Type['HomieStreamItem']:
        """
        Return the class object that was imported within method.

        :returns: Class object that was imported within method.
        """

        from .threads import (
            HomieStreamItem)

        return HomieStreamItem


    @classmethod
    def desired(
        cls,
    ) -> Type['HomieDesiredItem']:
        """
        Return the class object that was imported within method.

        :returns: Class object that was imported within method.
        """

        from .addons import (
            HomieDesiredItem)

        return HomieDesiredItem


    @classmethod
    def aspired(
        cls,
    ) -> Type['HomieAspiredItem']:
        """
        Return the class object that was imported within method.

        :returns: Class object that was imported within method.
        """

        from .addons import (
            HomieAspiredItem)

        return HomieAspiredItem
