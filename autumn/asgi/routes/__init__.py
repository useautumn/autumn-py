from __future__ import annotations

from typing import TYPE_CHECKING, Tuple, Any

if TYPE_CHECKING:
    from starlette.requests import Request
    from ...aio.client import AsyncClient
    from ..app import AutumnData


async def _extract(
    request: Request,
) -> Tuple[AutumnData, AsyncClient, Any]:
    autumn = getattr(request.app.state, "__autumn__")
    identify_func = autumn["identify"]
    client = autumn["client"]

    identify = await identify_func(request)
    json = await request.json()
    return (identify, client, json)
