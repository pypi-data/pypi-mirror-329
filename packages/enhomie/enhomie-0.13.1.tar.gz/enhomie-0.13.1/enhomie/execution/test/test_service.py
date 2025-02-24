"""
Functions and routines associated with Enasis Network Homie Automate.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from ..service import arguments



def test_arguments() -> None:
    """
    Perform various tests associated with relevant routines.
    """

    sargs = arguments([
        '--config', 'path'])

    assert sargs == {
        'config': 'path',
        'console': False,
        'debug': False,
        'dryrun': False,
        'potent': None,
        'faspires': None,
        'fdesires': None,
        'idesire': None,
        'iupdate': None,
        'dactions': None,
        'dstreams': None,
        'dupdates': None,
        'erestful': None,
        'atimeout': None,
        'utimeout': None,
        'stimeout': None,
        'paction': False,
        'pupdate': False,
        'pstream': False,
        'pdesire': False,
        'paspire': False}
