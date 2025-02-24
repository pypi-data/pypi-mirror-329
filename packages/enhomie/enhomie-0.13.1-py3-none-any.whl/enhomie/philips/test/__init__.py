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

from enconnect.philips.test import ByteStreamBlock

from httpx import Response

from respx import MockRouter



SAMPLES = (
    Path(__file__).parent
    / 'samples')



def mock_phue(
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
         'https://192.168.1.10'
         '/clip/v2/resource')
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
         'https://192.168.2.10'
         '/clip/v2/resource')
     .mock(Response(
         status_code=200,
         content=source)))


    samples = SAMPLES / 'stream'


    source = read_text(
        f'{samples}/source'
        '/jupiter.json')

    source = read_sample(
        sample=source,
        replace=replaces,
        prefix=False)

    streamer = (
        ByteStreamBlock(source))

    (respx_mock
     .get(
         'https://192.168.1.10'
         '/eventstream/clip/v2')
     .mock(Response(
         status_code=200,
         stream=streamer)))


    source = read_text(
        f'{samples}/source'
        '/neptune.json')

    source = read_sample(
        sample=source,
        replace=replaces,
        prefix=False)

    streamer = (
        ByteStreamBlock(source))

    (respx_mock
     .get(
         'https://192.168.2.10'
         '/eventstream/clip/v2')
     .mock(Response(
         status_code=200,
         stream=streamer)))


    match = compile(
        r'^https\S+\.168\.[12]\.10'
        r'\/clip/v2/resource/'
        r'(scene|grouped_|light)\S+$')

    (respx_mock
     .put(match)
     .mock(Response(200)))
