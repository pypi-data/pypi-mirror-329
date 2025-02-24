"""
Functions and routines associated with Enasis Network Homie Automate.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from typing import TYPE_CHECKING

from encommon.types import inrepr
from encommon.types import instr
from encommon.types import lattrs

if TYPE_CHECKING:
    from ...service import HomieService



def test_HomieUpdates(
    service: 'HomieService',
) -> None:
    """
    Perform various tests associated with relevant routines.

    :param service: Ancilary Homie Automate class instance.
    """

    assert service.updates

    member = service.updates


    attrs = lattrs(member)

    assert attrs == [
        '_HomieMember__homie',
        '_HomieMember__threads',
        '_HomieMember__aqueue',
        '_HomieMember__uqueue',
        '_HomieMember__squeue',
        '_HomieMember__vacate',
        '_HomieMember__cancel']


    assert inrepr(
        'updates.HomieUpdates',
        member)

    assert isinstance(
        hash(member), int)

    assert instr(
        'updates.HomieUpdates',
        member)


    assert member.homie

    assert len(member.threads) == 6

    assert member.aqueue

    assert member.uqueue

    assert member.squeue

    assert member.vacate

    assert member.cancel

    assert len(member.running) == 0


    member.operate()
