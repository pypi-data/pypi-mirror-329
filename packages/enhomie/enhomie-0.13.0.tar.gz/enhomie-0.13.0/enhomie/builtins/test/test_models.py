"""
Functions and routines associated with Enasis Network Homie Automate.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from ..models import BltnModels



def test_BltnModels_cover() -> None:
    """
    Perform various tests associated with relevant routines.
    """

    models = BltnModels

    drivers = models.drivers()

    assert drivers.store()
    assert drivers.period()
    assert drivers.regexp()
