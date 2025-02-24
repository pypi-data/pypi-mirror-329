"""
Functions and routines associated with Enasis Network Homie Automate.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from typing import TYPE_CHECKING

from fastapi.testclient import TestClient

if TYPE_CHECKING:
    from ..service import RestfulService
    from ...homie import Homie



def test_get_persists(
    homie: 'Homie',
    restful: 'RestfulService',
    client: TestClient,
) -> None:
    """
    Perform various tests associated with relevant routines.

    :param homie: Primary class instance for Homie Automate.
    :param restful: Ancilary Homie Automate class instance.
    :param client: Used when testing the FastAPI endpoints.
    """

    persist = homie.persist

    persist.insert(
        'jupiter_aspire',
        False)

    persist.insert(
        'neptune_aspire',
        False)


    path = '/api/persists'

    response = client.get(path)

    assert response.status_code == 200

    _response = response.json()

    entries = _response['entries']


    assert entries == [

        {'about': 'Aspire for Jupiter',
         'about_icon': 'jupiter',
         'about_label': 'Jupiter Aspire',
         'expire': None,
         'level': 'information',
         'tags': ['jupiter', 'aspire'],
         'unique': 'jupiter_aspire',
         'update': entries[0]['update'],
         'value': False,
         'value_icon': None,
         'value_label': 'Current Status',
         'value_unit': 'status'},

        {'about': 'Aspire for Neptune',
         'about_icon': 'neptune',
         'about_label': 'Neptune Aspire',
         'expire': None,
         'level': 'information',
         'tags': ['neptune', 'aspire'],
         'unique': 'neptune_aspire',
         'update': entries[1]['update'],
         'value': False,
         'value_icon': None,
         'value_label': 'Current Status',
         'value_unit': 'status'}]
