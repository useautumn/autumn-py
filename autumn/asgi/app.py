from __future__ import annotations

from typing import Coroutine, Callable, TypedDict, Any, TYPE_CHECKING

try:
    from starlette.routing import Router, Route
    from starlette.responses import JSONResponse
    from starlette.middleware import Middleware
    from starlette.middleware.base import BaseHTTPMiddleware
except ImportError:
    from ..error import AutumnError

    STARLETTE_INSTALLED = False

    raise AutumnError(
        "starlette is not installed. Please install it with `pip install starlette`",
        "missing_dependency",
    )
else:
    STARLETTE_INSTALLED = True

from .routes.core import (
    attach_route,
    check_route,
    track_route,
    cancel_route,
    billing_portal_route,
)
from .routes.customers import create_customer_route, pricing_table_route
from .routes.entities import create_entity_route, delete_entity_route, get_entity_route
from ..aio.client import AsyncClient
from ..error import AutumnHTTPError

if TYPE_CHECKING:
    from starlette.requests import Request


class _CustomerData(TypedDict):
    name: str
    email: str


class AutumnIdentifyData(TypedDict):
    customer_id: str
    customer_data: _CustomerData


class _StateMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, *, client, identify):
        super().__init__(app)
        self._client = client
        self._identify = identify

    async def dispatch(self, request: Request, call_next):
        request.state.__autumn__ = {
            "client": self._client,
            "identify": self._identify,
        }
        return await call_next(request)


class AutumnASGI:
    def __init__(
        self,
        token: str,
        *,
        identify: Callable[[Request], Coroutine[Any, Any, AutumnIdentifyData]],
    ):
        self._client = AsyncClient(token)
        self._identify = identify

        router = Router(
            routes=[
                Route("/attach", attach_route, methods={"POST"}),
                Route("/check/", check_route, methods={"POST"}),
                Route("/track/", track_route, methods={"POST"}),
                Route("/cancel/", cancel_route, methods={"POST"}),
                Route(
                    "/billing_portal/",
                    billing_portal_route,
                    methods={"POST"},
                ),
                Route(
                    "/customers/", create_customer_route, methods={"POST", "OPTIONS"}
                ),
                Route(
                    "/customers/{customer_id:str}/entities/{entity_id:str}",
                    delete_entity_route,
                    methods={"DELETE"},
                ),
                Route(
                    "/customers/{customer_id:str}/entities/",
                    create_entity_route,
                    methods={"POST"},
                ),
                Route(
                    "/customers/{customer_id:str}/entities/{entity_id:str}/",
                    get_entity_route,
                    methods={"GET"},
                ),
                Route(
                    "/components/pricing_table/",
                    pricing_table_route,
                    methods={"GET"},
                ),
            ],
            middleware=[
                Middleware(
                    _StateMiddleware, client=self._client, identify=self._identify
                )
            ],
        )
        self._router = router

    async def _handle_http_error(self, _: Request, exc: AutumnHTTPError):
        return JSONResponse({"detail": f"{exc.message} ({exc.code})"})

    async def close(self):
        await self._client.close()

    async def __call__(self, scope: Any, receive: Any, send: Any) -> None:
        try:
            await self._router(scope, receive, send)
        except AutumnHTTPError as exc:
            response = JSONResponse({"detail": str(exc)}, status_code=400)
            await response(scope, receive, send)
