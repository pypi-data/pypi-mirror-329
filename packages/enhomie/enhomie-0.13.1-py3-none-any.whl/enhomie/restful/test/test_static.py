"""
Functions and routines associated with Enasis Network Homie Automate.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from typing import TYPE_CHECKING

from encommon.types import instr

from fastapi.testclient import TestClient

if TYPE_CHECKING:
    from ..service import RestfulService



def test_get_static(
    restful: 'RestfulService',
    client: TestClient,
) -> None:
    """
    Perform various tests associated with relevant routines.

    :param restful: Ancilary Homie Automate class instance.
    :param client: Used when testing the FastAPI endpoints.
    """


    path = '/static/persist.html'

    response = client.get(path)

    assert response.status_code == 200

    assert instr(
        '<!DOCTYPE html>',
        response.text)


    path = '/static/doesnotexist'

    response = client.get(path)

    assert response.status_code == 403


    path = '/static/doesnotexist.html'

    response = client.get(path)

    assert response.status_code == 404


    path = '/static/styles/default'

    response = client.get(path)

    assert response.status_code == 200


    path = '/static/scripts/default'

    response = client.get(path)

    assert response.status_code == 200


    path = '/static/scripts/restful'

    response = client.get(path)

    assert response.status_code == 200


    path = '/static/images/success'

    response = client.get(path)

    assert response.status_code == 200


    path = '/static/images/motion'

    response = client.get(path)

    assert response.status_code == 200
