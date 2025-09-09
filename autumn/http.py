import sys
import time
import random
from typing import Dict, Type, TypeVar

import requests
from pydantic import BaseModel

from .utils import _build_model, _check_response, ExponentialBackoff
from .error import AutumnError, AutumnHTTPError

__all__ = ("HTTPClient",)

T = TypeVar("T", bound=BaseModel)


class _RetryRequestError(Exception):
    pass

class HTTPClient:
    def __init__(
        self,
        base_url: str,
        version: str,
        token: str,
        max_retries: int
    ):
        self.base_url = base_url
        self.version = version
        self.session = requests.Session()

        self._headers = self._build_headers(token)
        self.max_retries = max_retries

        rand = random.Random()
        rand.seed()
        self._rand = rand

    @staticmethod
    def _build_url(base_url: str, version: str, path: str) -> str:
        return f"{base_url}/{version}{path}"

    @staticmethod
    def _build_headers(token: str) -> Dict[str, str]:
        from . import __version__, LATEST_API_VERSION

        v_info = sys.version_info
        user_agent = (
            f"autumn-py/{__version__}"
            f" (Python {v_info.major}.{v_info.minor}.{v_info.micro})"
        )
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "User-Agent": user_agent,
            "Authorization": f"Bearer {token}",
            "X-Api-Version": LATEST_API_VERSION,
        }
        return headers

    def request(
        self,
        method: str,
        path: str,
        type_: Type[T],
        **kwargs,
    ) -> T:
        if self.session is None:
            raise AutumnError(
                "Session is not initialized. You may have closed the client accidentally.",
                "session_not_initialized",
            )

        url = self._build_url(self.base_url, self.version, path)

        max_retries = self.max_retries
        backoff = ExponentialBackoff()
        for attempt in range(self.max_retries):
            try:
                resp = self.session.request(
                    method,
                    url,
                    headers=self._headers,
                    **kwargs
                )
                if 500 <= resp.status_code <= 504:
                    raise _RetryRequestError()

                data = resp.json()
            except (
                _RetryRequestError,
                OSError,
                requests.ConnectionError,
                requests.ConnectTimeout
            ):
                if attempt == max_retries - 1:
                    raise

                time.sleep(backoff.bedtime)
                backoff.tick()
            else:
                _check_response(resp.status_code, data)
                return _build_model(type_, data)

        # We should never get here. This is to appease type checkers.
        msg = f"Max retries reached for {method} {path}"
        raise AutumnHTTPError(msg, "max_retries_reached", 500)

    def close(self):
        if self.session is not None:
            self.session.close()
            self.session = None
