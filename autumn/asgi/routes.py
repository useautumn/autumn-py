from __future__ import annotations

from typing import TYPE_CHECKING

from starlette.responses import JSONResponse

if TYPE_CHECKING:
    from starlette.requests import Request
    from ..aio.client import AsyncClient


async def attach_route(request: Request):
    data = await request.json()
    autumn: AsyncClient = request.state.autumn

    response = await autumn.attach(**data)
    return JSONResponse(response.model_dump(mode="json"))


async def check_route(request: Request):
    data = await request.json()
    autumn: AsyncClient = request.state.autumn

    response = await autumn.check(**data)
    return JSONResponse(response.model_dump(mode="json"))


async def track_route(request: Request):
    data = await request.json()
    autumn: AsyncClient = request.state.autumn

    response = await autumn.track(**data)
    return JSONResponse(response.model_dump(mode="json"))
