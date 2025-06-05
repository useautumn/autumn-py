from typing import Optional, List, Any, Dict

from .customers import Customers
from .http import HTTPClient
from .types import (
    AttachResponse,
    Feature,
    Customer,
    CheckResponse,
    TrackResponse,
)
from .utils import _build_payload


__all__ = ("Client",)


class Client:
    def __init__(self, token: str):
        from . import BASE_URL, VERSION

        self.http = HTTPClient(BASE_URL, VERSION, token)
        self.customers = Customers(self.http)

    def attach(
        self,
        customer_id: str,
        *,
        product_id: Optional[str] = None,
        product_ids: Optional[List[str]] = None,
        success_url: Optional[str] = None,
        force_checkout: bool = False,
        features: Optional[List[Feature]] = None,
        entity_id: Optional[str] = None,
        customer_data: Optional[Customer] = None,
        free_trial: Optional[bool] = None,
    ) -> AttachResponse:
        assert product_id is not None or product_ids is not None, (
            "Either product_id or product_ids must be provided"
        )
        assert not (product_id is not None and product_ids is not None), (
            "Only one of product_id or product_ids must be provided"
        )

        if product_id is not None:
            product_ids = [product_id]

        payload = _build_payload(locals(), self.attach, ignore={"product_id"})
        return self.http.request("POST", "/attach", AttachResponse, json=payload)

    def check(
        self,
        customer_id: str,
        *,
        product_id: Optional[str] = None,
        feature_id: Optional[str] = None,
        required_balance: Optional[int] = 1,
        send_event: bool = False,
        with_preview: bool = False,
        entity_id: Optional[str] = None,
        customer_data: Optional[Customer] = None,
    ) -> CheckResponse:
        assert product_id is not None or feature_id is not None, (
            "Either product_id or feature_id must be provided"
        )

        payload = _build_payload(locals(), self.check)
        return self.http.request("POST", "/check", CheckResponse, json=payload)

    def track(
        self,
        customer_id: str,
        feature_id: str,
        *,
        value: int = 1,
        entity_id: Optional[str] = None,
        event_name: Optional[str] = None,
        idempotency_key: Optional[str] = None,
        properties: Optional[Dict[str, Any]] = None,
        customer_data: Optional[Customer] = None,
    ) -> TrackResponse:
        payload = _build_payload(locals(), self.track)
        return self.http.request("POST", "/track", TrackResponse, json=payload)
