"""
Functions and routines associated with Enasis Network Homie Automate.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from typing import Annotated
from typing import Any
from typing import Optional

from encommon.times import unitime
from encommon.times.unitime import NOTATE

from pydantic import Field

from .common import HomieParamsModel
from ..addons.persist import HomiePersistLevel
from ..addons.persist import _PERSIST_ABOUT



_PARAM_VALUE_UNIT = Annotated[
    Optional[str],
    Field(None,
          description=_PERSIST_ABOUT['value_unit'],
          min_length=1)]

_PARAM_VALUE_LABEL = Annotated[
    Optional[str],
    Field(None,
          description=_PERSIST_ABOUT['value_label'],
          min_length=1)]

_PARAM_VALUE_ICON = Annotated[
    Optional[str],
    Field(None,
          description=_PERSIST_ABOUT['value_icon'],
          min_length=1)]

_PARAM_ABOUT = Annotated[
    Optional[str],
    Field(None,
          description=_PERSIST_ABOUT['about'],
          min_length=1)]

_PARAM_ABOUT_LABEL = Annotated[
    Optional[str],
    Field(None,
          description=_PERSIST_ABOUT['about_label'],
          min_length=1)]

_PARAM_ABOUT_ICON = Annotated[
    Optional[str],
    Field(None,
          description=_PERSIST_ABOUT['about_icon'],
          min_length=1)]

_PARAM_LEVEL = Annotated[
    Optional[HomiePersistLevel],
    Field(None,
          description=_PERSIST_ABOUT['level'],
          min_length=1)]

_PARAM_TAGS = Annotated[
    Optional[list[str]],
    Field(None,
          description=_PERSIST_ABOUT['tags'],
          min_length=1)]

_PARAM_EXPIRE = Annotated[
    Optional[str],
    Field(None,
          description=_PERSIST_ABOUT['expire'],
          pattern=NOTATE,
          examples=['1h', '1h30m', '1d'],
          min_length=1)]



class HomiePersistParams(HomieParamsModel, extra='forbid'):
    """
    Process and validate the Homie configuration parameters.
    """

    value_unit: _PARAM_VALUE_UNIT

    value_label: _PARAM_VALUE_LABEL

    value_icon: _PARAM_VALUE_ICON

    about: _PARAM_ABOUT

    about_label: _PARAM_ABOUT_LABEL

    about_icon: _PARAM_ABOUT_ICON

    level: _PARAM_LEVEL

    tags: _PARAM_TAGS

    expire: _PARAM_EXPIRE


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
