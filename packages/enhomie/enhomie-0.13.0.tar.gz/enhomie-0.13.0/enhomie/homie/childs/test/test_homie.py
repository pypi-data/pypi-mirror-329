"""
Functions and routines associated with Enasis Network Homie Automate.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from pathlib import Path
from typing import TYPE_CHECKING

from encommon.types import inrepr
from encommon.types import instr
from encommon.types import lattrs
from encommon.utils import save_text

from respx import MockRouter

from ....conftest import config_factory
from ....conftest import homie_factory

if TYPE_CHECKING:
    from ...homie import Homie



def test_HomieChilds(
    homie: 'Homie',
) -> None:
    """
    Perform various tests associated with relevant routines.

    :param homie: Primary class instance for Homie Automate.
    """

    childs = homie.childs


    attrs = lattrs(childs)

    assert attrs == [
        '_HomieChilds__homie',
        '_HomieChilds__origins',
        '_HomieChilds__devices',
        '_HomieChilds__groups',
        '_HomieChilds__scenes',
        '_HomieChilds__desires',
        '_HomieChilds__aspires']


    assert inrepr(
        'homie.HomieChilds',
        childs)

    assert isinstance(
        hash(childs), int)

    assert instr(
        'homie.HomieChilds',
        childs)


    childs.validate()

    assert childs.origins

    assert childs.devices

    assert childs.groups

    assert childs.scenes

    assert childs.desires

    assert childs.aspires



def test_HomieChilds_cover(
    tmp_path: Path,
    respx_mock: MockRouter,
) -> None:
    """
    Perform various tests associated with relevant routines.

    :param tmp_path: pytest object for temporal filesystem.
    :param respx_mock: Object for mocking request operation.
    """

    samples = (
        tmp_path / 'homie')

    samples.mkdir()

    save_text(
        samples / 'test.yml',
        """
        filters:
         desires:
          - neptune_*
         aspires:
          - neptune_*
        """)  # noqa: LIT003

    homie = homie_factory(
        config_factory(tmp_path),
        respx_mock=respx_mock)


    childs = homie.childs
    desires = childs.desires
    aspires = childs.aspires

    assert len(desires) == 3
    assert len(aspires) == 2
