import sys
from typing import Dict

import requests
from pydantic import BaseModel

from . import __version__

__all__ = ("HTTPClient",)


class HTTPClient:
    def __init__(self, base_url: str, version: str, token: str):
        self.base_url = base_url
        self.version = version
        self.session = requests.Session()

        self._headers = self._build_headers(token)

    @staticmethod
    def _build_url(base_url: str, version: str, path: str) -> str:
        return f"{base_url}/{version}{path}"

    @staticmethod
    def _build_headers(token: str) -> Dict[str, str]:
        v_info = sys.version_info
        user_agent = (
            f"autumn.py/{__version__} (https://github.com/justanotherbyte/autumn)"
            f" (Python {v_info.major}.{v_info.minor}.{v_info.micro})"
        )
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "User-Agent": user_agent,
            "Authorization": f"Bearer {token}",
        }
        return headers

    def request(
        self,
        method: str,
        path: str,
        type_: BaseModel,
        **kwargs,
    ) -> BaseModel:
        url = self._build_url(self.base_url, self.version, path)
        resp = self.session.request(method, url, headers=self._headers, **kwargs)

        resp.raise_for_status()

        data = resp.json()
        return type_.model_validate_json(data)
