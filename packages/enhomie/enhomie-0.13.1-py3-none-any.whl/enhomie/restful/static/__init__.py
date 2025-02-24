"""
Functions and routines associated with Enasis Network Homie Automate.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



import asyncio
from pathlib import Path
from typing import Optional

from encommon.types.strings import SEMPTY
from encommon.utils import read_text
from encommon.webkit import Content

from fastapi import APIRouter
from fastapi import HTTPException
from fastapi import Request
from fastapi import Response
from fastapi.responses import FileResponse



APIROUTER = APIRouter(
    tags=['Static Content'])

_STATIC = (
    Path(__file__).parents[1]
    / 'static')



@APIROUTER.get(
    '/static/images/{item}')
async def get_static_images(
    request: Request,
    item: str,
) -> Response:
    """
    Handle the API request and return using response model.

    :param item: Which item to locate and return contents.
    :returns: Response object containing relevant contents.
    """

    local = _static_file(
        f'{item}.svg', 'images')

    content = (
        Content.images(item)
        or SEMPTY)

    if local is not None:
        content = (
            read_text(local))

    await asyncio.sleep(0)

    return Response(
        content,
        media_type='image/svg+xml')



@APIROUTER.get(
    '/static/scripts/{item}')
async def get_static_scripts(
    request: Request,
    item: str,
) -> Response:
    """
    Handle the API request and return using response model.

    :param item: Which item to locate and return contents.
    :returns: Response object containing relevant contents.
    """

    local = _static_file(
        f'{item}.js', 'scripts')

    content = (
        Content.scripts(item)
        or SEMPTY)

    if local is not None:
        content += (
            '\n\n\n'
            f'{read_text(local)}')

    await asyncio.sleep(0)

    return Response(
        content,
        media_type='application/javascript')



@APIROUTER.get(
    '/static/styles/{item}')
async def get_static_styles(
    request: Request,
    item: str,
) -> Response:
    """
    Handle the API request and return using response model.

    :param item: Which item to locate and return contents.
    :returns: Response object containing relevant contents.
    """

    local = _static_file(
        f'{item}.css', 'styles')

    content = (
        Content.styles(item)
        or SEMPTY)

    if local is not None:
        content += (
            '\n\n\n'
            f'{read_text(local)}')

    await asyncio.sleep(0)

    return Response(
        content,
        media_type='text/css')



@APIROUTER.get(
    '/static/{file}')
async def get_static(
    request: Request,
    file: str,
) -> FileResponse:
    """
    Handle the API request and return using response model.

    :param file: Which file to locate and return contents.
    :returns: Response object containing relevant contents.
    """

    if file[-5:] != '.html':
        raise HTTPException(403)

    path = _static_file(file)

    if path is None:
        raise HTTPException(404)

    await asyncio.sleep(0)

    return FileResponse(path)



def _static_file(
    path: Path | str,
    base: Optional[str] = None,
) -> Optional[Path]:
    """
    Return the filesystem path object using the parameters.

    :param path: Complete or relative path for processing.
    :param base: Parent directory where the file is located.
    :returns: Filesystem path object using the parameters.
    """

    static = Path(_STATIC)

    if base is not None:
        static /= Path(base)

    static /= path

    if not static.exists():
        return None

    return static.resolve()
