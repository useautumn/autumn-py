from __future__ import annotations

from typing import TYPE_CHECKING

from . import _extract, _build_response

if TYPE_CHECKING:
    from starlette.requests import Request


async def list_products_route(request: Request):
    identify, autumn, _ = await _extract(request)

    customer_id = identify["customer_id"]

    response = await autumn.products.list(customer_id=customer_id)
    return _build_response(response)
