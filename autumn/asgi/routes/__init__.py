from __future__ import annotations

from typing import TYPE_CHECKING, Tuple, Any

if TYPE_CHECKING:
    from starlette.requests import Request
    from ...aio.client import AsyncClient
    from ..app import AutumnIdentifyData


async def _extract(
    request: Request,
    *,
    get_json: bool = True,
) -> Tuple[AutumnIdentifyData, AsyncClient, Any]:
    autumn = getattr(request.state, "__autumn__")
    identify_func = autumn["identify"]
    client = autumn["client"]

    identify = await identify_func(request)
    json = await request.json() if get_json else None
    return (identify, client, json)
