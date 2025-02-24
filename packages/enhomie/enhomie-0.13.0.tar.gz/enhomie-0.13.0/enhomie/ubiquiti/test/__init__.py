"""
Functions and routines associated with Enasis Network Homie Automate.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from pathlib import Path

from encommon.types import DictStrAny
from encommon.utils import read_sample
from encommon.utils import read_text

from httpx import Response

from respx import MockRouter



SAMPLES = (
    Path(__file__).parent
    / 'samples')



def mock_ubiq(
    respx_mock: MockRouter,
    replaces: DictStrAny,
) -> None:
    """
    Construct the mocker objects for simulating operations.

    :param respx_mock: Object for mocking request operation.
    :param replaces: Mapping of what to replace in samples.
    """

    samples = SAMPLES / 'origin'


    source = read_text(
        f'{samples}/source/'
        'jupiter/historic.json')

    source = read_sample(
        sample=source,
        replace=replaces,
        prefix=False)

    (respx_mock
     .get(
         'https://192.168.1.1'
         '/proxy/network/api/s'
         '/default/rest/user')
     .mock(Response(
         status_code=200,
         content=source)))


    source = read_text(
        f'{samples}/source/'
        'jupiter/realtime.json')

    source = read_sample(
        sample=source,
        replace=replaces,
        prefix=False)

    (respx_mock
     .get(
         'https://192.168.1.1'
         '/proxy/network/api/s'
         '/default/stat/sta')
     .mock(Response(
         status_code=200,
         content=source)))


    source = read_text(
        f'{samples}/source/'
        'neptune/historic.json')

    source = read_sample(
        sample=source,
        replace=replaces,
        prefix=False)

    (respx_mock
     .get(
         'https://192.168.2.1'
         '/proxy/network/api/s'
         '/default/rest/user')
     .mock(Response(
         status_code=200,
         content=source)))


    source = read_text(
        f'{samples}/source/'
        'neptune/realtime.json')

    source = read_sample(
        sample=source,
        replace=replaces,
        prefix=False)

    (respx_mock
     .get(
         'https://192.168.2.1'
         '/proxy/network/api/s'
         '/default/stat/sta')
     .mock(Response(
         status_code=200,
         content=source)))
