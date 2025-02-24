"""
Functions and routines associated with Enasis Network Homie Automate.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from typing import Annotated
from typing import Any

from pydantic import Field

from ...homie.params.common import HomieParamsModel



class DriverBltnRegexpParams(HomieParamsModel, extra='forbid'):
    """
    Process and validate the Homie configuration parameters.
    """

    patterns: Annotated[
        list[str],
        Field(...,
              description='Regular expression match',
              min_length=1)]

    complete: Annotated[
        bool,
        Field(False,
              description='Perform complete match')]


    def __init__(
        # NOCVR
        self,
        /,
        **data: Any,
    ) -> None:
        """
        Initialize instance for class using provided parameters.
        """

        patterns = data.get('patterns')

        if isinstance(patterns, str):
            data['patterns'] = [patterns]

        super().__init__(**data)
