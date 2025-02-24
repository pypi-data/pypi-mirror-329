"""
Functions and routines associated with Enasis Network Homie Automate.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from typing import Literal

from ..homie.childs import HomieDevice



class HubiDevice(HomieDevice):
    """
    Contain the relevant attributes from the related source.
    """


    @property
    def family(
        self,
    ) -> Literal['hubitat']:
        """
        Return the value for the attribute from class instance.

        :returns: Value for the attribute from class instance.
        """

        return 'hubitat'
