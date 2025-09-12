from __future__ import annotations

from typing import TYPE_CHECKING

from ...utils import _build_payload as _build_kwargs
from ...models.meta import CustomerData
from . import _build_response, _extract

if TYPE_CHECKING:
    from starlette.requests import Request


async def attach_route(request: Request):
    identify, autumn, json = await _extract(request)

    customer_id = identify["customer_id"]
    customer_data = identify["customer_data"]

    kwargs = _build_kwargs(json, autumn.attach)

    response = await autumn.attach(
        customer_id, customer_data=CustomerData(**customer_data), **kwargs
    )
    return _build_response(response)


async def check_route(request: Request):
    identify, autumn, json = await _extract(request)

    customer_id = identify["customer_id"]
    kwargs = _build_kwargs(json, autumn.check)

    response = await autumn.check(customer_id, **kwargs)
    return _build_response(response)


async def track_route(request: Request):
    identify, autumn, json = await _extract(request)

    customer_id = identify["customer_id"]
    kwargs = _build_kwargs(json, autumn.track)

    response = await autumn.track(customer_id, **kwargs)
    return _build_response(response)


async def cancel_route(request: Request):
    identify, autumn, json = await _extract(request)

    customer_id = identify["customer_id"]
    kwargs = _build_kwargs(json, autumn.cancel)

    response = await autumn.cancel(customer_id, **kwargs)
    return _build_response(response)


async def billing_portal_route(request: Request):
    identify, autumn, json = await _extract(request)

    customer_id = identify["customer_id"]
    kwargs = _build_kwargs(
        json,
        autumn.customers.get_billing_portal,
    )
    response = await autumn.customers.get_billing_portal(customer_id, **kwargs)
    return _build_response(response)


async def checkout_route(request: Request):
    identify, autumn, json = await _extract(request)

    customer_id = identify["customer_id"]
    kwargs = _build_kwargs(json, autumn.checkout)

    response = await autumn.checkout(customer_id, **kwargs)
    return _build_response(response)


async def query_route(request: Request):
    identify, autumn, json = await _extract(request)

    customer_id = identify["customer_id"]
    kwargs = _build_kwargs(json, autumn.query)

    response = await autumn.query(customer_id=customer_id, **kwargs)
    return _build_response(response)
