"""
Functions and routines associated with Enasis Network Homie Automate.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from argparse import ArgumentParser
from sys import argv as sys_argv
from typing import Optional
from typing import TYPE_CHECKING
from typing import get_args

from encommon.types import DictStrAny

from ..homie import Homie
from ..homie import HomieConfig
from ..homie.common import HomieState

if TYPE_CHECKING:
    from ..homie.childs import HomieDevice
    from ..homie.childs import HomieGroup
    from ..homie.childs import HomieScene



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
        '--print',
        action='store_true',
        default=False,
        dest='paction',
        help=(
            'print the submited '
            'actions to console'))


    parser.add_argument(
        '--group',
        help=(
            'which group action '
            'is performed upon'))


    parser.add_argument(
        '--device',
        help=(
            'which device action '
            'is performed upon'))


    states = list(
        get_args(HomieState))

    parser.add_argument(
        '--state',
        choices=states,
        help=(
            'which state value the '
            'target will changed'))


    parser.add_argument(
        '--color',
        help=(
            'which color value the '
            'target will changed'))


    parser.add_argument(
        '--level',
        type=int,
        help=(
            'which level value the '
            'target will changed'))


    parser.add_argument(
        '--scene',
        help=(
            'which level value the '
            'target will changed'))


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

    assert homie.refresh()

    config = homie.config
    sargs = config.sargs

    _group = sargs['group']
    _device = sargs['device']
    _scene = sargs['scene']

    childs = homie.childs
    devices = childs.devices
    groups = childs.groups
    scenes = childs.scenes
    potent = homie.potent


    group: Optional['HomieGroup']
    device: Optional['HomieDevice']
    scene: Optional['HomieScene']

    group = (
        groups[_group]
        if _group is not None
        else None)

    device = (
        devices[_device]
        if _device is not None
        else None)

    scene = (
        scenes[_scene]
        if _scene is not None
        else None)


    target = device or group

    assert target is not None


    aitems = (
        homie.get_actions(
            target=target,
            state=sargs['state'],
            color=sargs['color'],
            level=sargs['level'],
            scene=scene))

    homie.set_actions(
        aitems=aitems,
        force=potent)



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
        base='execution/action',
        status='started')

    homie = Homie(config)

    operation(homie)

    config.logger.log_i(
        base='execution/action',
        status='stopped')

    config.logger.stop()



if __name__ == '__main__':
    execution()  # NOCVR
