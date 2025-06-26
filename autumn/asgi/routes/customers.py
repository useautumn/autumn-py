from __future__ import annotations

from typing import TYPE_CHECKING

from starlette.responses import JSONResponse

from . import _extract

if TYPE_CHECKING:
    from starlette.requests import Request


async def create_customer_route(request: Request):
    identify, autumn, _ = await _extract(request)

    customer_id = identify["customer_id"]
    customer_data = identify["customer_data"]
    response = await autumn.customers.create(customer_id, **customer_data)
    return JSONResponse(response.model_dump(mode="json"))


async def pricing_table_route(request: Request):
    identify, autumn, _ = await _extract(request, get_json=False)

    customer_id = identify["customer_id"]
    response = await autumn.customers.pricing_table(customer_id)
    return JSONResponse(response.model_dump(mode="json"))
