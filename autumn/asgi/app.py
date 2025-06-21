from __future__ import annotations

from typing import Coroutine, Callable, TypedDict, Any, TYPE_CHECKING

from starlette.routing import Router, Route
from starlette.responses import JSONResponse

from .routes.core import (
    attach_route,
    check_route,
    track_route,
    cancel_route,
    billing_portal_route,
)
from .routes.customers import create_customer_route
from .routes.entities import create_entity_route, delete_entity_route
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


class AutumnASGI:
    def __init__(
        self,
        token: str,
        *,
        identify: Callable[[Request], Coroutine[Any, Any, AutumnIdentifyData]],
    ):
        router = Router(
            routes=[
                Route("/attach/", attach_route, methods={"POST", "OPTIONS"}),
                Route("/check/", check_route, methods={"POST", "OPTIONS"}),
                Route("/track/", track_route, methods={"POST", "OPTIONS"}),
                Route("/cancel/", cancel_route, methods={"POST", "OPTIONS"}),
                Route(
                    "/billing_portal/",
                    billing_portal_route,
                    methods={"POST", "OPTIONS"},
                ),
                Route(
                    "/customers/", create_customer_route, methods={"POST", "OPTIONS"}
                ),
                Route(
                    "/entities/{entity_id}/",
                    delete_entity_route,
                    methods={"DELETE"},
                ),
                Route("/entities/{entity_id}", create_entity_route, methods={"POST"}),
            ],
        )
        self._router = router
        self._identify = identify
        self._client = AsyncClient(token)

    def setup(self, app: Any):
        app.state.__autumn__ = {"client": self._client, "identify": self._identify}

    async def _handle_http_error(self, request: Request, exc: AutumnHTTPError):
        return JSONResponse({"detail": f"{exc.message} ({exc.code})"})

    async def __call__(self, scope: Any, receive: Any, send: Any) -> None:
        try:
            await self._router(scope, receive, send)
        except AutumnHTTPError as exc:
            response = JSONResponse({"detail": str(exc)}, status_code=400)
            await response(scope, receive, send)
