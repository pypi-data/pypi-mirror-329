"""
Functions and routines associated with Enasis Network Homie Automate.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



import asyncio
from typing import Annotated

from encommon.times import Time
from encommon.types import BaseModel

from fastapi import APIRouter
from fastapi import Request

from pydantic import Field

from ..homie.addons import HomiePersistRecord



APIROUTER = APIRouter(
    tags=['Persistent Values'])



class HomiePersistEntries(BaseModel, extra='forbid'):
    """
    Contain the information regarding the persistent values.
    """

    entries: Annotated[
        list[HomiePersistRecord],
        Field(...,
              description='Entries related to the request')]

    elapsed: Annotated[
        float,
        Field(...,
              description='Seconds elapsed since request')]



@APIROUTER.get(
    '/api/persists',
    response_model=HomiePersistEntries)
async def get_persists(
    request: Request,
) -> HomiePersistEntries:
    """
    Handle the API request and return using response model.
    """

    runtime = Time('now')

    homie = request.app.homie
    persist = homie.persist

    await asyncio.sleep(0)

    entries = sorted(
        persist.records(),
        key=lambda x: x.unique)

    return HomiePersistEntries(
        entries=entries,
        elapsed=runtime.since)
