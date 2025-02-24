"""
Functions and routines associated with Enasis Network Homie Automate.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from ..models import PhueModels



def test_PhueModels_cover() -> None:
    """
    Perform various tests associated with relevant routines.
    """

    models = PhueModels

    assert models.origin()
    assert models.action()
    assert models.update()
    assert models.stream()

    drivers = models.drivers()

    assert drivers.button()
    assert drivers.change()
    assert drivers.contact()
    assert drivers.motion()

    helpers = drivers.helpers()

    assert callable(
        helpers.sensors())
    assert callable(
        helpers.changed())
    assert callable(
        helpers.current())
