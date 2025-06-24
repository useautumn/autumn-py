from typing import Type, TypeVar

from pydantic import BaseModel

from ..error import AutumnError
from ..http import HTTPClient
from ..utils import _build_model, _check_response


try:
    import aiohttp
except ImportError:
    raise AutumnError(
        "aiohttp is not installed. Please install it with `pip install aiohttp`",
        "missing_dependency",
    )

T = TypeVar("T", bound=BaseModel)


__all__ = ("AsyncHTTPClient",)


class AsyncHTTPClient:
    def __init__(self, base_url: str, version: str, token: str):
        self.base_url = base_url
        self.version = version
        self.session = None  # type: ignore
        self._headers = HTTPClient._build_headers(token)

        self._build_url = HTTPClient._build_url

    def _ensure_session(self):
        if self.session is None:
            self.session = aiohttp.ClientSession()

    async def request(self, method: str, path: str, type_: Type[T], **kwargs) -> T:
        self._ensure_session()
        assert self.session is not None  # appease type checker

        url = self._build_url(self.base_url, self.version, path)

        async with self.session.request(
            method, url, headers=self._headers, **kwargs
        ) as resp:
            data = await resp.json()

        _check_response(resp.status, data)
        return _build_model(type_, data)

    async def close(self):
        if self.session is not None:
            await self.session.close()
