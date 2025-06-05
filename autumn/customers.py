from __future__ import annotations

from typing import (
    Optional,
    Dict,
    Any,
    TypeVar,
    Generic,
    overload,
    Coroutine,
    TYPE_CHECKING,
)

from .types.customers import Customer
from .utils import _build_payload

if TYPE_CHECKING:
    from .http import HTTPClient
    from .aio.http import AsyncHTTPClient

T_HttpClient = TypeVar("T_HttpClient", "AsyncHTTPClient", "HTTPClient")

__all__ = ("Customers",)


class Customers(Generic[T_HttpClient]):
    def __init__(self, http: T_HttpClient):
        self._http = http

    @overload
    def get(self: "Customers[HTTPClient]", customer_id: str) -> Customer: ...

    @overload
    def get(
        self: "Customers[AsyncHTTPClient]", customer_id: str
    ) -> Coroutine[Any, Any, Customer]: ...

    def get(self, customer_id):
        return self._http.request("GET", f"/customers/{customer_id}", Customer)

    @overload
    def create(
        self: "Customers[HTTPClient]",
        id: str,
        *,
        email: Optional[str] = None,
        name: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Customer: ...

    @overload
    def create(
        self: "Customers[AsyncHTTPClient]",
        id: str,
        *,
        email: Optional[str] = None,
        name: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Coroutine[Any, Any, Customer]: ...

    def create(
        self,
        id: str,
        *,
        email: Optional[str] = None,
        name: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ):
        payload = _build_payload(locals(), self.create)  # type: ignore
        return self._http.request("POST", "/customers", Customer, json=payload)
