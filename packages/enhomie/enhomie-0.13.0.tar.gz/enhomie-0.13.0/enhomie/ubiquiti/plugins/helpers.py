"""
Functions and routines associated with Enasis Network Homie Automate.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from typing import TYPE_CHECKING

from encommon.times import Time

from ...utils import UnexpectedCondition

if TYPE_CHECKING:
    from ..helpers import UbiqFetch



def ubiq_latest(
    source: 'UbiqFetch',
) -> Time:
    """
    Return the timestamp for client association with router.

    :param source: Dictionary of parameters from the bridge.
    :returns: Timestamp for client association with router.
    """


    gwsecs = (
        source
        .get('_uptime_by_ugw'))

    apsecs = (
        source
        .get('_uptime_by_uap'))

    if (gwsecs is not None
            or apsecs is not None):
        return Time()


    laseen = (
        source
        .get('last_seen'))

    if laseen is not None:
        return Time(laseen[0])


    raise UnexpectedCondition
