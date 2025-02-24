"""
Functions and routines associated with Enasis Network Homie Automate.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ...homie import Homie



def test_HomieChild_cover(
    homie: 'Homie',
) -> None:
    """
    Perform various tests associated with relevant routines.

    :param homie: Primary class instance for Homie Automate.
    """

    childs = homie.childs
    origins = childs.origins

    child1 = origins[
        'neptune_philips']

    child2 = origins[
        'jupiter_philips']


    sort = [child1, child2]

    assert sorted(sort) == [
        child2, child1]
