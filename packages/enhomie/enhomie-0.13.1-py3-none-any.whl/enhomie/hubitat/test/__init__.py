"""
Functions and routines associated with Enasis Network Homie Automate.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from pathlib import Path
from re import compile

from encommon.types import DictStrAny
from encommon.utils import read_sample
from encommon.utils import read_text

from httpx import Response

from respx import MockRouter



SAMPLES = (
    Path(__file__).parent
    / 'samples')



def mock_hubi(
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
        f'{samples}/source'
        '/jupiter.json')

    source = read_sample(
        sample=source,
        replace=replaces,
        prefix=False)

    (respx_mock
     .get(
         'https://192.168.1.11'
         '/apps/api/69'
         '/devices/all')
     .mock(Response(
         status_code=200,
         content=source)))


    source = read_text(
        f'{samples}/source'
        '/neptune.json')

    source = read_sample(
        sample=source,
        replace=replaces,
        prefix=False)

    (respx_mock
     .get(
         'https://192.168.2.11'
         '/apps/api/69'
         '/devices/all')
     .mock(Response(
         status_code=200,
         content=source)))


    match = compile(
        r'^https\S+\.168\.[12]\.11'
        r'\/apps\/api\/69\/devices'
        r'\/\d+\/(set|on|off)(.*|)$')

    (respx_mock
     .get(match)
     .mock(Response(200)))
