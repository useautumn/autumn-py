from __future__ import annotations

from typing import TYPE_CHECKING

from . import _build_response, _extract

if TYPE_CHECKING:
    from starlette.requests import Request


async def create_entity_route(request: Request):
    _, autumn, json = await _extract(request)

    customer_id = request.path_params["customer_id"]
    response = await autumn.entities.create(customer_id=customer_id, **json)

    return _build_response(response)


async def delete_entity_route(request: Request):
    _, autumn, _ = await _extract(request)

    customer_id = request.path_params["customer_id"]
    entity_id = request.path_params["entity_id"]
    response = await autumn.entities.delete(customer_id, entity_id)

    return _build_response(response)


async def get_entity_route(request: Request):
    _, autumn, _ = await _extract(request)

    customer_id = request.path_params["customer_id"]
    entity_id = request.path_params["entity_id"]
    expand = request.query_params.get("expand", None)

    if expand is not None:
        expand = expand.split(",")

    response = await autumn.entities.get(customer_id, entity_id, expand=expand)  # type: ignore
    return _build_response(response)
