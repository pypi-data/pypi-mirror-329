"""
Functions and routines associated with Enasis Network Homie Automate.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from ..models import HubiModels



def test_HubiModels_cover() -> None:
    """
    Perform various tests associated with relevant routines.
    """

    models = HubiModels

    assert models.origin()
    assert models.action()
    assert models.update()
