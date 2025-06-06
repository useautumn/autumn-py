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
from .types.response import BillingPortalResponse
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

    @overload
    def update(
        self: "Customers[HTTPClient]",
        customer_id: str,
        *,
        name: Optional[str] = None,
        email: Optional[str] = None,
        fingerprint: Optional[str] = None,
    ) -> Customer: ...

    @overload
    def update(
        self: "Customers[AsyncHTTPClient]",
        customer_id: str,
        *,
        name: Optional[str] = None,
        email: Optional[str] = None,
        fingerprint: Optional[str] = None,
    ) -> Coroutine[Any, Any, Customer]: ...

    def update(
        self,
        customer_id: str,
        *,
        name: Optional[str] = None,
        email: Optional[str] = None,
        fingerprint: Optional[str] = None,
    ):
        payload = _build_payload(locals(), self.update, ignore={"customer_id"})  # type: ignore
        return self._http.request(
            "POST", f"/customers/{customer_id}", Customer, json=payload
        )

    @overload
    def get_billing_portal(
        self: "Customers[HTTPClient]",
        customer_id: str,
        *,
        return_url: Optional[str] = None,
    ) -> BillingPortalResponse: ...

    @overload
    def get_billing_portal(
        self: "Customers[AsyncHTTPClient]",
        customer_id: str,
        *,
        return_url: Optional[str] = None,
    ) -> Coroutine[Any, Any, BillingPortalResponse]: ...

    def get_billing_portal(
        self,
        customer_id: str,
        *,
        return_url: Optional[str] = None,
    ):
        payload = _build_payload(
            locals(),
            self.get_billing_portal,  # type: ignore
            ignore={"customer_id"},
        )
        return self._http.request(
            "POST",
            f"/customers/{customer_id}/billing_portal",
            BillingPortalResponse,
            json=payload,
        )
