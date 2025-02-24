"""
Functions and routines associated with Enasis Network Homie Automate.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from typing import TYPE_CHECKING

from encommon.types import inrepr
from encommon.types import instr
from encommon.types import lattrs

from ..queue import HomieQueue
from ..queue import HomieQueueItem

if TYPE_CHECKING:
    from ...homie import Homie



def test_HomieQueueItem() -> None:
    """
    Perform various tests associated with relevant routines.
    """

    item = HomieQueueItem()

    assert item.time.since < 1



def test_HomieQueue(
    homie: 'Homie',
) -> None:
    """
    Perform various tests associated with relevant routines.

    :param homie: Primary class instance for Homie Automate.
    """

    _queue = HomieQueue[
        HomieQueueItem]

    item = HomieQueueItem()


    queue: _queue = (
        HomieQueue(homie))


    attrs = lattrs(queue)

    assert attrs == [
        '_HomieQueue__homie',
        '_HomieQueue__queue']


    assert inrepr(
        'queue.HomieQueue',
        queue)

    assert isinstance(
        hash(queue), int)

    assert instr(
        'queue.HomieQueue',
        queue)


    assert queue.empty

    assert queue.qsize == 0


    queue.put(item)

    assert not queue.empty

    assert queue.qsize == 1

    _item = queue.get()

    assert queue.empty

    assert queue.qsize == 0

    assert item == _item
