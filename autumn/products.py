from __future__ import annotations

from typing import (
    List,
    Any,
    TypeVar,
    Generic,
    overload,
    Coroutine,
    Optional,
    TYPE_CHECKING,
)

from .types.products import ProductItem, FreeTrial
from .types.response import (
    CreateProductResponse,
    GetProductResponse,
    ReferralCodeResponse,
    ReferralRedeemResponse,
    ProductCancelResponse,
)
from .utils import _build_payload

if TYPE_CHECKING:
    from .http import HTTPClient
    from .aio.http import AsyncHTTPClient

T_HttpClient = TypeVar("T_HttpClient", "AsyncHTTPClient", "HTTPClient")


class Products(Generic[T_HttpClient]):
    def __init__(self, http: T_HttpClient):
        self._http = http

    @overload
    def create_product(
        self: "Products[HTTPClient]",
        id: str,
        *,
        name: str,
        is_add_on: bool = False,
        is_default: bool = False,
        items: Optional[List[ProductItem]] = None,
        free_trial: Optional[FreeTrial] = None,
    ) -> CreateProductResponse: ...

    @overload
    def create_product(
        self: "Products[AsyncHTTPClient]",
        id: str,
        *,
        name: str,
        is_add_on: bool = False,
        is_default: bool = False,
        items: Optional[List[ProductItem]] = None,
        free_trial: Optional[FreeTrial] = None,
    ) -> Coroutine[Any, Any, CreateProductResponse]: ...

    def create_product(
        self,
        id: str,
        *,
        name: str,
        is_add_on: bool = False,
        is_default: bool = False,
        items: Optional[List[ProductItem]] = None,
        free_trial: Optional[FreeTrial] = None,
    ):
        payload = _build_payload(locals(), self.create_product)  # type: ignore
        return self._http.request(
            "POST", "/products", CreateProductResponse, json=payload
        )

    @overload
    def get_product(
        self: "Products[HTTPClient]",
        id: str,
    ) -> GetProductResponse: ...

    @overload
    def get_product(
        self: "Products[AsyncHTTPClient]",
        id: str,
    ) -> Coroutine[Any, Any, GetProductResponse]: ...

    def get_product(self, id: str):
        return self._http.request("GET", f"/products/{id}", GetProductResponse)

    @overload
    def get_referral_code(
        self: "Products[HTTPClient]",
        customer_id: str,
        program_id: str,
    ) -> ReferralCodeResponse: ...

    @overload
    def get_referral_code(
        self: "Products[AsyncHTTPClient]",
        customer_id: str,
        program_id: str,
    ) -> Coroutine[Any, Any, ReferralCodeResponse]: ...

    def get_referral_code(
        self,
        customer_id: str,
        program_id: str,
    ):
        payload = _build_payload(locals(), self.get_referral_code)  # type: ignore
        return self._http.request(
            "POST",
            "/referrals/code",
            ReferralCodeResponse,
            json=payload,
        )

    @overload
    def redeem_referral_code(
        self: "Products[HTTPClient]",
        code: str,
        customer_id: str,
        reward_id: str,
    ) -> ReferralRedeemResponse: ...

    @overload
    def redeem_referral_code(
        self: "Products[AsyncHTTPClient]",
        code: str,
        customer_id: str,
        reward_id: str,
    ) -> Coroutine[Any, Any, ReferralRedeemResponse]: ...

    def redeem_referral_code(
        self,
        code: str,
        customer_id: str,
        reward_id: str,
    ):
        payload = _build_payload(locals(), self.redeem_referral_code)  # type: ignore
        return self._http.request(
            "POST",
            "/referrals/redeem",
            ReferralRedeemResponse,
            json=payload,
        )

    @overload
    def cancel_product(
        self: "Products[HTTPClient]",
        customer_id: str,
        product_id: str,
        entity_id: Optional[str] = None,
    ) -> ProductCancelResponse: ...

    @overload
    def cancel_product(
        self: "Products[AsyncHTTPClient]",
        customer_id: str,
        product_id: str,
        entity_id: Optional[str] = None,
    ) -> Coroutine[Any, Any, ProductCancelResponse]: ...

    def cancel_product(
        self,
        customer_id: str,
        product_id: str,
        entity_id: Optional[str] = None,
    ):
        payload = _build_payload(locals(), self.cancel_product)  # type: ignore
        return self._http.request(
            "POST",
            "/products/cancel",
            ProductCancelResponse,
            json=payload,
        )
