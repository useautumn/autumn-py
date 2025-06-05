from typing import Optional, List, Any, Dict, Callable

from pydantic import BaseModel

from .http import HTTPClient
from .types import (
    AttachResponse,
    Feature,
    Customer,
    CheckResponse,
    TrackResponse,
)


BASE_URL = "https://api.useautumn.com"
VERSION = "v1"


def _build_payload(scope: Dict[str, Any], method: Callable) -> Dict[str, Any]:
    params = method.__code__.co_varnames
    payload: Dict[str, Any] = {}

    for key, value in scope.items():
        if key != "self" and key in params:
            payload[key] = (
                value.model_dump_json() if isinstance(value, BaseModel) else value
            )

    return payload


class Client:
    def __init__(self, token: str):
        self.http = HTTPClient(BASE_URL, VERSION, token)

    def attach(
        self,
        customer_id: str,
        product_id: str,
        *,
        product_ids: Optional[List[str]] = None,
        success_url: Optional[str] = None,
        force_checkout: bool = False,
        features: Optional[List[Feature]] = None,
        entity_id: Optional[str] = None,
        customer_data: Optional[Customer] = None,
    ) -> AttachResponse:
        payload = _build_payload(locals(), self.attach)
        return self.http.request("POST", "/attach", AttachResponse, json=payload)  # type: ignore

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
        return self.http.request("POST", "/check", CheckResponse, json=payload)  # type: ignore

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
        return self.http.request("POST", "/track", TrackResponse, json=payload)  # type: ignore
