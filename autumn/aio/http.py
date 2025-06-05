from typing import Type

from pydantic import BaseModel

from ..error import AutumnError
from ..http import HTTPClient


class _AsyncHTTPClient:
    def __init__(self, base_url: str, version: str, token: str):
        self.base_url = base_url
        self.version = version
        self.session = None  # type: ignore
        self._headers = HTTPClient._build_headers(token)

        self._build_url = HTTPClient._build_url

    def _ensure_session(self):
        if self.session is None:
            self.session = aiohttp.ClientSession()  # type: ignore

    async def request(
        self, method: str, path: str, type_: BaseModel, **kwargs
    ) -> BaseModel:
        self._ensure_session()
        assert self.session is not None  # appease type checker

        url = self._build_url(self.base_url, self.version, path)

        async with self.session.request(
            method, url, headers=self._headers, **kwargs
        ) as resp:
            resp.raise_for_status()
            data = await resp.json()

        return type_.model_validate_json(data)

    async def close(self):
        if self.session is not None:
            await self.session.close()


AsyncHTTPClient: Type[_AsyncHTTPClient]

try:
    import aiohttp
except ImportError:
    AsyncHTTPClient = None  # type: ignore
    raise AutumnError(
        "aiohttp is not installed. Please install it with `pip install aiohttp`",
        "missing_dependency",
    )
else:
    AsyncHTTPClient = _AsyncHTTPClient
