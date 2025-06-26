from __future__ import annotations

from typing import TYPE_CHECKING

from starlette.responses import JSONResponse

from . import _extract
from ...types.meta import CustomerData

if TYPE_CHECKING:
    from starlette.requests import Request


async def attach_route(request: Request):
    identify, autumn, json = await _extract(request)

    customer_id = identify["customer_id"]
    customer_data = identify["customer_data"]

    response = await autumn.attach(
        customer_id, customer_data=CustomerData(**customer_data), **json
    )
    return JSONResponse(response.model_dump(mode="json"))


async def check_route(request: Request):
    identify, autumn, json = await _extract(request)

    customer_id = identify["customer_id"]
    response = await autumn.check(customer_id, **json)
    return JSONResponse(response.model_dump(mode="json"))


async def track_route(request: Request):
    identify, autumn, json = await _extract(request)

    customer_id = identify["customer_id"]
    response = await autumn.track(customer_id, **json)
    return JSONResponse(response.model_dump(mode="json"))


async def cancel_route(request: Request):
    identify, autumn, json = await _extract(request)

    customer_id = identify["customer_id"]
    response = await autumn.products.cancel(customer_id, **json)
    return JSONResponse(response.model_dump(mode="json"))


async def billing_portal_route(request: Request):
    identify, autumn, json = await _extract(request)

    customer_id = identify["customer_id"]
    response = await autumn.customers.get_billing_portal(customer_id, **json)
    return JSONResponse(response.model_dump(mode="json"))
