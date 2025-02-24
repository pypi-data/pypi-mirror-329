"""
Functions and routines associated with Enasis Network Homie Automate.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from typing import Annotated
from typing import Any

from encommon.times import unitime

from pydantic import Field

from .common import HomieParamsModel
from .persist import _PARAM_ABOUT
from .persist import _PARAM_ABOUT_ICON
from .persist import _PARAM_ABOUT_LABEL
from .persist import _PARAM_EXPIRE
from .persist import _PARAM_LEVEL
from .persist import _PARAM_TAGS
from .persist import _PARAM_VALUE_ICON
from .persist import _PARAM_VALUE_LABEL
from .persist import _PARAM_VALUE_UNIT
from ..addons.persist import HomiePersistValue
from ..addons.persist import _PERSIST_ABOUT



_PARAM_UNIQUE = Annotated[
    str,
    Field(...,
          description=_PERSIST_ABOUT['unique'],
          min_length=1)]

_PARAM_VALUE = Annotated[
    HomiePersistValue,
    Field(...,
          description=_PERSIST_ABOUT['value'])]



class HomieStoreParams(HomieParamsModel, extra='forbid'):
    """
    Process and validate the Homie configuration parameters.
    """

    unique: _PARAM_UNIQUE

    value: _PARAM_VALUE

    value_unit: _PARAM_VALUE_UNIT

    value_label: _PARAM_VALUE_LABEL

    value_icon: _PARAM_VALUE_ICON

    about: _PARAM_ABOUT

    about_label: _PARAM_ABOUT_LABEL

    about_icon: _PARAM_ABOUT_ICON

    level: _PARAM_LEVEL

    tags: _PARAM_TAGS

    expire: _PARAM_EXPIRE = '1d'


    def __init__(
        # NOCVR
        self,
        /,
        **data: Any,
    ) -> None:
        """
        Initialize instance for class using provided parameters.
        """

        tags = data.get('tags')
        expire = data.get('expire')

        if isinstance(tags, str):
            data['tags'] = [tags]

        if isinstance(expire, str):
            expire = unitime(expire)
            assert expire >= 0

        super().__init__(**data)
