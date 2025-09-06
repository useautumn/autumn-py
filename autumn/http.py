import sys
from typing import Dict, Type, TypeVar

import requests
from pydantic import BaseModel

from .error import AutumnError
from .utils import _build_model, _check_response

__all__ = ("HTTPClient",)

T = TypeVar("T", bound=BaseModel)


class HTTPClient:
    def __init__(
        self,
        base_url: str,
        version: str,
        token: str,
    ):
        self.base_url = base_url
        self.version = version
        self.session = requests.Session()

        self._headers = self._build_headers(token)

    @staticmethod
    def _build_url(base_url: str, version: str, path: str) -> str:
        return f"{base_url}/{version}{path}"

    @staticmethod
    def _build_headers(
        token: str,
    ) -> Dict[str, str]:
        from . import (
            LATEST_API_VERSION,
            __version__,
        )

        v_info = sys.version_info
        user_agent = f"autumn-py/{__version__}" f" (Python {v_info.major}.{v_info.minor}.{v_info.micro})"
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
        resp = self.session.request(
            method,
            url,
            headers=self._headers,
            **kwargs,
        )

        data = resp.json()

        _check_response(resp.status_code, data)
        return _build_model(type_, data)

    def close(self):
        if self.session is not None:
            self.session.close()
            self.session = None
