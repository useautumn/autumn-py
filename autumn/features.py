from __future__ import annotations

from typing import (
    List,
    Any,
    TypeVar,
    Generic,
    overload,
    Coroutine,
    TYPE_CHECKING,
)

from .types.balance import Balance
from .types.meta import Empty
from .utils import _build_payload

if TYPE_CHECKING:
    from .http import HTTPClient
    from .aio.http import AsyncHTTPClient


T_HttpClient = TypeVar("T_HttpClient", "AsyncHTTPClient", "HTTPClient")


class Features(Generic[T_HttpClient]):
    def __init__(self, http: T_HttpClient):
        self._http = http

    @overload
    def set_usage(
        self: "Features[HTTPClient]", customer_id: str, feature_id: str, value: int
    ) -> Empty: ...

    @overload
    def set_usage(
        self: "Features[AsyncHTTPClient]", customer_id: str, feature_id: str, value: int
    ) -> Coroutine[Any, Any, Empty]: ...

    def set_usage(self, customer_id: str, feature_id: str, value: int):
        payload = _build_payload(locals(), self.set_usage, ignore={"customer_id"})  # type: ignore
        return self._http.request(
            "POST",
            f"/customers/{customer_id}/balances",
            Empty,
            json=payload,
        )

    @overload
    def set_balances(
        self: "Features[HTTPClient]",
        customer_id: str,
        balances: List[Balance],
    ) -> Empty: ...

    @overload
    def set_balances(
        self: "Features[AsyncHTTPClient]",
        customer_id: str,
        balances: List[Balance],
    ) -> Coroutine[Any, Any, Empty]: ...

    def set_balances(self, customer_id: str, balances: List[Balance]):
        payload = _build_payload(locals(), self.set_balances, ignore={"customer_id"})  # type: ignore
        return self._http.request(
            "POST", f"/customers/{customer_id}/balances", Empty, json=payload
        )

    @overload
    def create_entity(
        self: "Features[HTTPClient]",
        customer_id: str,
        id: str,
        feature_id: str,
        name: str,
    ) -> Empty: ...

    @overload
    def create_entity(
        self: "Features[AsyncHTTPClient]",
        customer_id: str,
        id: str,
        feature_id: str,
        name: str,
    ) -> Coroutine[Any, Any, Empty]: ...

    def create_entity(self, customer_id: str, id: str, feature_id: str, name: str):
        payload = _build_payload(locals(), self.create_entity, ignore={"customer_id"})  # type: ignore
        return self._http.request(
            "POST", f"/customers/{customer_id}/entities", Empty, json=payload
        )

    @overload
    def delete_entity(
        self: "Features[HTTPClient]",
        customer_id: str,
        entity_id: str,
    ) -> Empty: ...

    @overload
    def delete_entity(
        self: "Features[AsyncHTTPClient]",
        customer_id: str,
        entity_id: str,
    ) -> Coroutine[Any, Any, Empty]: ...

    def delete_entity(self, customer_id: str, entity_id: str):
        return self._http.request(
            "DELETE", f"/customers/{customer_id}/entities/{entity_id}", Empty
        )
