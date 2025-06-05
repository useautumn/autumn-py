from .http import AsyncHTTPClient

from .shed import AttachParams, CheckParams, TrackParams
from ..client import BASE_URL, VERSION
from ..client import Client as _Client

__all__ = ("Client",)


class _AsyncClient(_Client):
    attach: AttachParams  # type: ignore
    check: CheckParams  # type: ignore
    track: TrackParams  # type: ignore

    def __init__(self, token: str):
        self.http = AsyncHTTPClient(BASE_URL, VERSION, token)

    async def close(self):
        await self.http.close()


Client = _AsyncClient
