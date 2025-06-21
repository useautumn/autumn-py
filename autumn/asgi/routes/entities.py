from __future__ import annotations

from typing import TYPE_CHECKING

from starlette.responses import JSONResponse

from . import _extract

if TYPE_CHECKING:
    from starlette.requests import Request


async def create_entity_route(request: Request):
    identify, autumn, json = await _extract(request)

    customer_id = identify["customer_id"]
    response = await autumn.features.create_entity(customer_id=customer_id, **json)

    return JSONResponse(response.model_dump(mode="json"))


async def delete_entity(request: Request):
    identify, autumn, json = await _extract(request)

    customer_id = identify["customer_id"]
    entity_id = json["identity_id"]
    response = await autumn.features.delete_entity(customer_id, entity_id)

    return JSONResponse(response.model_dump(mode="json"))
