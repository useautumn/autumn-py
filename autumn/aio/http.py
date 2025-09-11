import asyncio
from typing import Optional, Type, TypeVar

from pydantic import BaseModel

from ..error import AutumnError, AutumnHTTPError
from ..http import HTTPClient, _RetryRequestError
from ..utils import ExponentialBackoff, _build_model, _check_response

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
    def __init__(
        self,
        base_url: str,
        version: str,
        token: str,
        attempts: int,
        *,
        session: Optional[aiohttp.ClientSession] = None,
    ):
        self.base_url = base_url
        self.version = version
        self.session = session  # type: ignore
        self._headers = HTTPClient._build_headers(token)
        self.attempts = attempts

        self._build_url = HTTPClient._build_url

    async def request(
        self, method: str, path: str, type_: Type[T], **kwargs
    ) -> T:
        if self.session is None:
            self.session = aiohttp.ClientSession()

        url = self._build_url(self.base_url, self.version, path)

        max_attempts = self.attempts
        backoff = ExponentialBackoff()
        for attempt in range(max_attempts):
            try:
                async with self.session.request(
                    method, url, headers=self._headers, **kwargs
                ) as resp:
                    if 500 <= resp.status <= 504:
                        raise _RetryRequestError()

                    data = await resp.json()

            except (_RetryRequestError, OSError, asyncio.TimeoutError):
                if attempt == max_attempts - 1:
                    raise

                await asyncio.sleep(backoff.bedtime)
                backoff.tick()
            else:
                _check_response(resp.status, data)
                return _build_model(type_, data)

        # We should never get here. This is to appease type checkers.
        msg = f"Max retries reached for {method} {path}"
        raise AutumnHTTPError(msg, "max_retries_reached", 500)

    async def close(self):
        if self.session is not None:
            await self.session.close()
