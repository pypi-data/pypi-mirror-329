"""
Functions and routines associated with Enasis Network Homie Automate.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from ..models import HomieModels



def test_HomieModels_cover() -> None:
    """
    Perform various tests associated with relevant routines.
    """

    models = HomieModels

    assert models.homie()
    assert models.printer()
    assert models.service()

    assert models.builtins()
    assert models.hubitat()
    assert models.philips()
    assert models.ubiquiti()

    assert models.child()
    assert models.origin()
    assert models.device()
    assert models.group()
    assert models.scene()
    assert models.desire()
    assert models.aspire()
    assert models.plugin()
    assert models.occur()
    assert models.where()

    assert models.stage()
    assert models.queue()
    assert models.thread()
    assert models.action()
    assert models.update()
    assert models.stream()
    assert models.desired()
    assert models.aspired()
