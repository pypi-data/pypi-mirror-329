"""
Functions and routines associated with Enasis Network Homie Automate.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from typing import Annotated
from typing import Optional

from pydantic import Field

from .plugin import HomiePluginParams
from ...builtins.params import DriverBltnPeriodParams
from ...builtins.params import DriverBltnStoreParams
from ...philips.params import DriverPhueChangeParams
from ...ubiquiti.params import DriverUbiqClientParams



class HomieWhereParams(HomiePluginParams, extra='forbid'):
    """
    Process and validate the Homie configuration parameters.

    .. note::
       When using the `default` `family`, the conditons are
       in an `AND` relationship. If another name is given
       for `family`, those will be with an OR relationship.
    """

    negate: Annotated[
        bool,
        Field(False,
              description='Invert conditional outcome')]

    family: Annotated[
        str,
        Field('default',
              description='Combine conditions in group',
              min_length=1)]

    builtins_store: Annotated[
        Optional[DriverBltnStoreParams],
        Field(None,
              description='Plugin for the operations')]

    builtins_period: Annotated[
        Optional[DriverBltnPeriodParams],
        Field(None,
              description='Plugin for the operations')]

    philips_change: Annotated[
        Optional[DriverPhueChangeParams],
        Field(None,
              description='Plugin for the operations')]

    ubiquiti_client: Annotated[
        Optional[DriverUbiqClientParams],
        Field(None,
              description='Plugin for the operations')]
