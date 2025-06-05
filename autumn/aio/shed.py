import typing

from ..types import Feature, Customer, AttachResponse, CheckResponse, TrackResponse


class AttachParams(typing.Protocol):
    def __call__(
        self,
        customer_id: str,
        product_id: str,
        *,
        product_ids: typing.Optional[typing.List[str]] = None,
        success_url: typing.Optional[str] = None,
        force_checkout: bool = False,
        features: typing.Optional[typing.List[Feature]] = None,
        entity_id: typing.Optional[str] = None,
        customer_data: typing.Optional[Customer] = None,
    ) -> typing.Awaitable[AttachResponse]: ...


class CheckParams(typing.Protocol):
    def __call__(
        self,
        customer_id: str,
        *,
        product_id: typing.Optional[str] = None,
        feature_id: typing.Optional[str] = None,
        required_balance: typing.Optional[int] = 1,
        send_event: bool = False,
        with_preview: bool = False,
        entity_id: typing.Optional[str] = None,
        customer_data: typing.Optional[Customer] = None,
    ) -> typing.Awaitable[CheckResponse]: ...


class TrackParams(typing.Protocol):
    def __call__(
        self,
        customer_id: str,
        feature_id: str,
        *,
        value: int = 1,
        entity_id: typing.Optional[str] = None,
        event_name: typing.Optional[str] = None,
        idempotency_key: typing.Optional[str] = None,
        properties: typing.Optional[typing.Dict[str, typing.Any]] = None,
        customer_data: typing.Optional[Customer] = None,
    ) -> typing.Awaitable[TrackResponse]: ...
