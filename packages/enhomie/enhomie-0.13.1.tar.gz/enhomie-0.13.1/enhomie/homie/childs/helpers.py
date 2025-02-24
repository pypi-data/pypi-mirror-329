"""
Functions and routines associated with Enasis Network Homie Automate.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from typing import TYPE_CHECKING
from typing import Union

from encommon.times import Time

if TYPE_CHECKING:
    from .aspire import HomieAspire
    from .desire import HomieDesire
    from ..threads import HomieStreamItem



_OCCURD_WHENS = list[bool]

_WHERE_WHENS = dict[str, bool]
_WHERE_WHENL = dict[str, list[bool]]



def whered(
    desire: Union['HomieDesire', 'HomieAspire'],
    time: Time,
) -> tuple[bool, ...]:
    """
    Return the boolean indicating the conditional outcomes.

    :param desire: Child class instance for Homie Automate.
    :param time: Time that will be used in the conditionals.
    :returns: Boolean indicating the conditional outcomes.
    """

    plugins = desire.wheres

    wheres: _WHERE_WHENS = {}


    lists: _WHERE_WHENL = {}

    for plugin in plugins:

        params = plugin.params
        negate = params.negate
        family = params.family

        if family not in lists:
            lists[family] = []

        _lists = lists[family]

        when = plugin.when(time)

        if negate is True:
            when = not when

        _lists.append(when)


    items = lists.items()

    for name, values in items:

        value = any(values)

        if name == 'default':
            value = all(values)

        wheres[name] = value


    _wheres = wheres.values()

    return tuple(_wheres)



def occurd(
    aspire: 'HomieAspire',
    sitem: 'HomieStreamItem',
) -> tuple[bool, ...]:
    """
    Return the boolean indicating the conditional outcomes.

    :param aspire: Child class instance for Homie Automate.
    :param sitem: Item containing information for operation.
    :returns: Boolean indicating the conditional outcomes.
    """

    plugins = aspire.occurs

    occurs: _OCCURD_WHENS = []


    for plugin in plugins:

        when = plugin.when(sitem)

        occurs.append(when)


    return tuple(occurs)
