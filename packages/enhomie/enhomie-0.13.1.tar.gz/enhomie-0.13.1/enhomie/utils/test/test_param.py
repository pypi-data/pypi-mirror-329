"""
Functions and routines associated with Enasis Network Homie Automate.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from typing import TYPE_CHECKING

from encommon.types import inrepr
from encommon.types import instr
from encommon.types import lattrs

from ..param import InvalidParam

if TYPE_CHECKING:
    from ...homie import Homie



def test_InvalidParam(
    homie: 'Homie',
) -> None:
    """
    Perform various tests associated with relevant routines.

    :param homie: Primary class instance for Homie Automate.
    """

    childs = homie.childs
    devices = childs.devices

    device = devices[
        'jupiter_motion']


    raises = InvalidParam(
        error='invalid',
        about='about',
        child=device,
        param='param',
        value='value')


    attrs = lattrs(raises)

    assert attrs == [
        'error',
        'about',
        'child',
        'param',
        'value']


    assert inrepr(
        'InvalidParam',
        raises)

    assert isinstance(
        hash(raises), int)

    assert instr(
        'Error (invalid)',
        raises)


    assert str(raises) == (
        'Error (invalid) '
        'param (param) '
        'value (value) child '
        '(PhueDevice'
        '/jupiter_motion)'
        ' (about)')
