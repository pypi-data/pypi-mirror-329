"""
Functions and routines associated with Enasis Network Homie Automate.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from ..action import arguments



def test_arguments() -> None:
    """
    Perform various tests associated with relevant routines.
    """

    sargs = arguments([
        '--config', 'path',
        '--group', 'group',
        '--scene', 'scene'])

    assert sargs == {
        'config': 'path',
        'console': False,
        'debug': False,
        'dryrun': False,
        'potent': None,
        'paction': False,
        'group': 'group',
        'device': None,
        'state': None,
        'color': None,
        'level': None,
        'scene': 'scene'}
