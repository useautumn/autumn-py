import contextlib
import posixpath

from starlette.routing import Router, Route

from .routes import attach_route, check_route, track_route
from ..aio.client import AsyncClient


class AutumnASGI:
    def __init__(self, *, token: str, base_path: str = "/api/autumn"):
        @contextlib.asynccontextmanager
        async def lifespan(_):
            async with AsyncClient(token=token) as client:
                yield {"autumn": client}

        def _(path: str):
            return posixpath.join(base_path, path.lstrip("/"))

        router = Router(
            lifespan=lifespan,
            routes=[
                Route(_("/attach"), attach_route, methods={"POST"}),
                Route(_("/check"), check_route, methods={"POST"}),
                Route(_("/track"), track_route, methods={"POST"}),
            ],
        )
        self._router = router

    async def __call__(self, scope, receive, send):
        await self._router(scope, receive, send)
