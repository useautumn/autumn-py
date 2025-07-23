from __future__ import annotations

from typing import TYPE_CHECKING

from . import _extract, _build_response
from ...models.meta import CustomerData

if TYPE_CHECKING:
    from starlette.requests import Request


async def attach_route(request: Request):
    identify, autumn, json = await _extract(request)

    customer_id = identify["customer_id"]
    customer_data = identify["customer_data"]

    response = await autumn.attach(
        customer_id, customer_data=CustomerData(**customer_data), **json
    )
    return _build_response(response)


async def check_route(request: Request):
    identify, autumn, json = await _extract(request)

    customer_id = identify["customer_id"]
    response = await autumn.check(customer_id, **json)
    return _build_response(response)


async def track_route(request: Request):
    identify, autumn, json = await _extract(request)

    customer_id = identify["customer_id"]
    response = await autumn.track(customer_id, **json)
    return _build_response(response)


async def cancel_route(request: Request):
    identify, autumn, json = await _extract(request)

    customer_id = identify["customer_id"]
    response = await autumn.products.cancel(customer_id, **json)
    return _build_response(response)


async def billing_portal_route(request: Request):
    identify, autumn, json = await _extract(request)

    customer_id = identify["customer_id"]
    response = await autumn.customers.get_billing_portal(customer_id, **json)
    return _build_response(response)
