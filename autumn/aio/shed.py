from __future__ import annotations

from typing import TYPE_CHECKING, Protocol

from autumn.models.response import CheckoutResponse

if TYPE_CHECKING:
    from typing import Optional, List, Awaitable, Dict, Any

    from ..models.meta import AttachOption
    from ..models.features import Feature
    from ..models.meta import CustomerData
    from ..models.response import (
        AttachResponse,
        CheckResponse,
        TrackResponse,
        CheckoutResponse,
    )

__all__ = ("AttachParams", "CheckParams", "TrackParams")


class AttachParams(Protocol):

    def __call__(
        self,
        customer_id: str,
        *,
        product_id: Optional[str] = None,
        product_ids: Optional[List[str]] = None,
        success_url: Optional[str] = None,
        force_checkout: bool = False,
        entity_id: Optional[str] = None,
        customer_data: Optional[CustomerData] = None,
        free_trial: Optional[bool] = None,
        options: Optional[List[AttachOption]] = None,
    ) -> Awaitable[AttachResponse]:
        ...


class CheckParams(Protocol):

    def __call__(
        self,
        customer_id: str,
        *,
        product_id: Optional[str] = None,
        feature_id: Optional[str] = None,
        required_balance: Optional[int] = 1,
        send_event: bool = False,
        with_preview: bool = False,
        entity_id: Optional[str] = None,
        customer_data: Optional[CustomerData] = None,
    ) -> Awaitable[CheckResponse]:
        ...


class TrackParams(Protocol):

    def __call__(
        self,
        customer_id: str,
        *,
        feature_id: Optional[str] = None,
        value: int = 1,
        entity_id: Optional[str] = None,
        event_name: Optional[str] = None,
        idempotency_key: Optional[str] = None,
        properties: Optional[Dict[str, Any]] = None,
        customer_data: Optional[CustomerData] = None,
    ) -> Awaitable[TrackResponse]:
        ...


class CheckoutParams(Protocol):

    def __call__(
        self,
        customer_id: str,
        *,
        product_id: Optional[str] = None,
        entity_id: Optional[str] = None,
        options: Optional[List[AttachOption]] = None,
        customer_data: Optional[CustomerData] = None,
        success_url: Optional[str] = None,
        checkout_session_params: Optional[Dict[str, Any]] = None,
        reward: Optional[str] = None,
    ) -> Awaitable[CheckoutResponse]:
        ...
