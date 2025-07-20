import random
import asyncio
from typing import Type, TypeVar

from pydantic import BaseModel

from ..error import AutumnError, AutumnHTTPError
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


class _RetryRequestError(Exception):
    pass


class AsyncHTTPClient:
    def __init__(self, base_url: str, version: str, token: str, max_retries: int = 3):
        self.base_url = base_url
        self.version = version
        self.session = None  # type: ignore
        self._headers = HTTPClient._build_headers(token)
        self.max_retries = max_retries

        self._build_url = HTTPClient._build_url

        rand = random.Random()
        rand.seed()
        self._rand = rand

    async def request(self, method: str, path: str, type_: Type[T], **kwargs) -> T:
        if self.session is None:
            self.session = aiohttp.ClientSession()

        url = self._build_url(self.base_url, self.version, path)

        for attempt in range(self.max_retries):
            try:
                async with self.session.request(
                    method, url, headers=self._headers, **kwargs
                ) as resp:
                    if 500 <= resp.status <= 504:
                        raise _RetryRequestError()

                    data = await resp.json()

            except (_RetryRequestError, OSError, asyncio.TimeoutError):
                sleep_time = (2 ** attempt) + self._rand.uniform(0, 1)
                await asyncio.sleep(sleep_time)
            else:
                _check_response(resp.status, data)
                return _build_model(type_, data)

        msg = f"Max retries reached for {method} {path}"
        raise AutumnHTTPError(msg, "max_retries_reached", 500)

    async def close(self):
        if self.session is not None:
            await self.session.close()
