"""
Functions and routines associated with Enasis Network Homie Automate.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from argparse import ArgumentParser
from signal import SIGHUP
from signal import SIGINT
from signal import SIGTERM
from signal import signal
from sys import argv as sys_argv
from typing import Optional

from encommon.types import DictStrAny

from ..homie import Homie
from ..homie import HomieConfig
from ..homie import HomieService



def arguments(  # noqa: CFQ001
    args: Optional[list[str]] = None,
) -> DictStrAny:
    """
    Construct arguments which are associated with the file.

    :param args: Override the source for the main arguments.
    :returns: Construct arguments from command line options.
    """

    parser = ArgumentParser()

    args = args or sys_argv[1:]


    parser.add_argument(
        '--config',
        required=True,
        help=(
            'complete or relative '
            'path to config file'))


    parser.add_argument(
        '--console',
        action='store_true',
        default=False,
        help=(
            'write log messages '
            'to standard output'))


    parser.add_argument(
        '--debug',
        action='store_true',
        default=False,
        help=(
            'increase logging level '
            'for standard output'))


    parser.add_argument(
        '--dry-run',
        action='store_true',
        default=False,
        dest='dryrun',
        help='do not execute actions')


    parser.add_argument(
        '--idempotent',
        action='store_false',
        default=None,
        dest='potent',
        help=(
            'do not make requests '
            'when already applied'))


    parser.add_argument(
        '--respite_desire',
        type=int,
        dest='idesire',
        help=(
            'override the interval '
            'for desires schedule'))


    parser.add_argument(
        '--respite_update',
        type=int,
        dest='iupdate',
        help=(
            'override the interval '
            'for updates schedule'))


    parser.add_argument(
        '--timeout_action',
        type=int,
        dest='atimeout',
        help=(
            'override the time '
            'for action request'))


    parser.add_argument(
        '--timeout_update',
        type=int,
        dest='utimeout',
        help=(
            'override the time '
            'for update request'))


    parser.add_argument(
        '--timeout_stream',
        type=int,
        dest='stimeout',
        help=(
            'override the timeout '
            'for stream request'))


    parser.add_argument(
        '--print_action',
        action='store_true',
        default=False,
        dest='paction',
        help=(
            'print the submited '
            'actions to console'))


    parser.add_argument(
        '--print_update',
        action='store_true',
        default=False,
        dest='pupdate',
        help=(
            'print the streamed '
            'updates to console'))


    parser.add_argument(
        '--print_stream',
        action='store_true',
        default=False,
        dest='pstream',
        help=(
            'print the streamed '
            'events to console'))


    parser.add_argument(
        '--print_desire',
        action='store_true',
        default=False,
        dest='pdesire',
        help=(
            'print the desired '
            'state to console'))


    parser.add_argument(
        '--print_aspire',
        action='store_true',
        default=False,
        dest='paspire',
        help=(
            'print the desired '
            'state to console'))


    parser.add_argument(
        '--filter_desires',
        type=lambda x: x.split(','),
        dest='fdesires',
        help=(
            'filter which desired '
            'objects are created'))


    parser.add_argument(
        '--filter_aspires',
        type=lambda x: x.split(','),
        dest='faspires',
        help=(
            'filter which aspired '
            'objects are created'))


    parser.add_argument(
        '--disable_actions',
        action='store_true',
        default=None,
        dest='dactions',
        help=(
            'override the boolean '
            'for enabling member'))

    parser.add_argument(
        '--disable_updates',
        action='store_true',
        default=None,
        dest='dupdates',
        help=(
            'override the boolean '
            'for enabling member'))

    parser.add_argument(
        '--disable_streams',
        action='store_true',
        default=None,
        dest='dstreams',
        help=(
            'override the boolean '
            'for enabling member'))

    parser.add_argument(
        '--enable_restful',
        action='store_true',
        default=None,
        dest='erestful',
        help=(
            'override the boolean '
            'for enabling member'))


    return vars(
        parser
        .parse_args(args))



def operation(
    # NOCVR
    homie: Homie,
) -> None:
    """
    Perform whatever operation is associated with the file.

    :param homie: Primary class instance for Homie Automate.
    """

    service = HomieService(homie)

    service.start()

    signal(SIGINT, service.soft)
    signal(SIGTERM, service.soft)
    signal(SIGHUP, service.soft)

    service.operate()



def execution(
    # NOCVR
    args: Optional[list[str]] = None,
) -> None:
    """
    Perform whatever operation is associated with the file.

    :param args: Override the source for the main arguments.
    """

    config = HomieConfig(
        arguments(args))

    config.logger.start()

    config.logger.log_i(
        base='execution/service',
        status='started')

    homie = Homie(config)

    operation(homie)

    config.logger.log_i(
        base='execution/service',
        status='stopped')

    config.logger.stop()



if __name__ == '__main__':
    execution()  # NOCVR
