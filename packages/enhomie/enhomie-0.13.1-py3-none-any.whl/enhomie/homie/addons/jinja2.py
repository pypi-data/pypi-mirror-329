"""
Functions and routines associated with Enasis Network Homie Automate.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from typing import TYPE_CHECKING

from encommon.parse import Jinja2
from encommon.parse.jinja2 import FILTERS
from encommon.types import DictStrAny

from ..models import HomieModels

if TYPE_CHECKING:
    from ..homie import Homie



class HomieJinja2(Jinja2):
    """
    Parse the provided input and intelligently return value.

    :param homie: Primary class instance for Homie Automate.
    """


    def __init__(
        self,
        homie: 'Homie',
    ) -> None:
        """
        Initialize instance for class using provided parameters.
        """


        statics: DictStrAny = {
            'homie': homie}

        filters: FILTERS = {
            'average': lambda x: (
                sum(x) / len(x))}

        models = HomieModels

        philips = (
            models.philips()
            .drivers().helpers())

        ubiquiti = (
            models.ubiquiti()
            .drivers().helpers())

        filters |= {
            'philips_sensors': (
                philips.sensors()),
            'philips_changed': (
                philips.changed()),
            'philips_current': (
                philips.current()),
            'ubiquiti_latest': (
                ubiquiti.latest())}

        super().__init__(
            statics=statics,
            filters=filters)
