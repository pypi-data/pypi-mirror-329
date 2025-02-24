"""
Functions and routines associated with Enasis Network Homie Automate.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from ..persist import arguments



def test_arguments() -> None:
    """
    Perform various tests associated with relevant routines.
    """

    sargs = arguments([
        '--config', 'path',
        '--unique', 'key'])

    assert sargs == {
        'config': 'path',
        'console': False,
        'debug': False,
        'expire': '30m',
        'unique': 'key',
        'value': None,
        'value_unit': None,
        'value_label': None,
        'value_icon': None,
        'about': None,
        'about_label': None,
        'about_icon': None,
        'level': None,
        'tags': None}
