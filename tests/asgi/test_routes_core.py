from unittest.mock import AsyncMock

import pytest
from pydantic import BaseModel
from starlette.responses import JSONResponse

from autumn.asgi.routes import core
from autumn.client import Client
from autumn.models.response import AttachResponse, CheckResponse, TrackResponse


DUMMY_CUSTOMER_ID = "user_123"
DUMMY_AUTUMN_SECRET_KEY = "sk_test_a1b2c3d4e5f6g7h8i9j0"
DUMMY_IDENTIFY_RETURN_VALUE = {"customer_id": DUMMY_CUSTOMER_ID, "customer_data": {}}


class DummyRequest:
    def __init__(self, state_obj):
        self.state = state_obj
        self._json = None

    async def json(self):
        return getattr(self, "_json", None)


def _setup_http_mock(autumn: Client, mock_response: BaseModel | None) -> None:
    autumn.http.request = AsyncMock(return_value=mock_response)  # type: ignore


def _prepare_request(
    json_payload=None, mock_response: BaseModel | None = None
) -> DummyRequest:
    autumn = Client(token=DUMMY_AUTUMN_SECRET_KEY)

    _setup_http_mock(autumn, mock_response)

    identify = AsyncMock(return_value=DUMMY_IDENTIFY_RETURN_VALUE)
    autumn_obj = {"identify": identify, "client": autumn}

    State = type("State", (), {})
    state_obj = State()
    setattr(state_obj, "__autumn__", autumn_obj)

    request = DummyRequest(state_obj)
    if json_payload is not None:
        request._json = json_payload

    return request


@pytest.mark.asyncio
async def test_attach_route_with_product_id():
    json_payload = {"product_id": "product_123"}

    mock_response = AttachResponse(
        code="success",
        message="Attached",
        checkout_url="https://checkout.example.com",
        customer_id=DUMMY_CUSTOMER_ID,
        product_ids=["product_123"],
    )

    request = _prepare_request(json_payload, mock_response)

    response = await core.attach_route(request)  # type: ignore

    assert isinstance(response, JSONResponse)


@pytest.mark.asyncio
async def test_attach_route_with_product_id_camel_case():
    json_payload = {"productId": "product_123"}

    mock_response = AttachResponse(
        code="success",
        message="Attached",
        checkout_url="https://checkout.example.com",
        customer_id=DUMMY_CUSTOMER_ID,
        product_ids=["product_123"],
    )

    request = _prepare_request(json_payload, mock_response)

    response = await core.attach_route(request)  # type: ignore

    assert isinstance(response, JSONResponse)


@pytest.mark.asyncio
async def test_attach_route_with_product_ids():
    json_payload = {"product_ids": ["product_123", "product_456"]}

    mock_response = AttachResponse(
        code="success",
        message="Attached",
        checkout_url="https://checkout.example.com",
        customer_id=DUMMY_CUSTOMER_ID,
        product_ids=["product_123", "product_456"],
    )

    request = _prepare_request(json_payload, mock_response)

    response = await core.attach_route(request)  # type: ignore

    assert isinstance(response, JSONResponse)


@pytest.mark.asyncio
async def test_attach_route_with_product_ids_camel_case():
    json_payload = {"productIds": ["product_123", "product_456"]}

    mock_response = AttachResponse(
        code="success",
        message="Attached",
        checkout_url="https://checkout.example.com",
        customer_id=DUMMY_CUSTOMER_ID,
        product_ids=["product_123", "product_456"],
    )

    request = _prepare_request(json_payload, mock_response)

    response = await core.attach_route(request)  # type: ignore

    assert isinstance(response, JSONResponse)


@pytest.mark.asyncio
async def test_attach_route_without_product_id_or_product_ids():
    json_payload = {}

    request = _prepare_request(json_payload)

    try:
        await core.attach_route(request)  # type: ignore
        assert False, "Should have raised AssertionError"
    except AssertionError as e:
        assert "Either product_id or product_ids must be provided" in str(e)


@pytest.mark.asyncio
async def test_check_route_with_product_id():
    json_payload = {"product_id": "product_123"}

    mock_response = CheckResponse(
        allowed=True,
        code="success",
        balance=100.0,
        customer_id=DUMMY_CUSTOMER_ID,
    )

    request = _prepare_request(json_payload, mock_response)

    response = await core.check_route(request)  # type: ignore

    assert isinstance(response, JSONResponse)


@pytest.mark.asyncio
async def test_check_route_with_product_id_camel_case():
    json_payload = {"productId": "product_123"}

    mock_response = CheckResponse(
        allowed=True,
        code="success",
        balance=100.0,
        customer_id=DUMMY_CUSTOMER_ID,
    )

    request = _prepare_request(json_payload, mock_response)

    response = await core.check_route(request)  # type: ignore

    assert isinstance(response, JSONResponse)


@pytest.mark.asyncio
async def test_check_route_with_feature_id():
    json_payload = {"feature_id": "feature_123"}

    mock_response = CheckResponse(
        allowed=True,
        code="success",
        balance=100.0,
        customer_id=DUMMY_CUSTOMER_ID,
    )

    request = _prepare_request(json_payload, mock_response)

    response = await core.check_route(request)  # type: ignore

    assert isinstance(response, JSONResponse)


@pytest.mark.asyncio
async def test_check_route_with_feature_id_camel_case():
    json_payload = {"featureId": "feature_123"}

    mock_response = CheckResponse(
        allowed=True,
        code="success",
        balance=100.0,
        customer_id=DUMMY_CUSTOMER_ID,
    )

    request = _prepare_request(json_payload, mock_response)

    response = await core.check_route(request)  # type: ignore

    assert isinstance(response, JSONResponse)


@pytest.mark.asyncio
async def test_check_route_without_product_id_or_feature_id():
    json_payload = {}

    request = _prepare_request(json_payload)

    try:
        await core.check_route(request)  # type: ignore
        assert False, "Should have raised AssertionError"
    except AssertionError as e:
        assert "Either product_id or feature_id must be provided" in str(e)


@pytest.mark.asyncio
async def test_track_route_with_feature_id():
    json_payload = {"feature_id": "feature_123"}

    mock_response = TrackResponse(
        id="track_123",
        code="success",
        customer_id=DUMMY_CUSTOMER_ID,
        feature_id="feature_123",
    )

    request = _prepare_request(json_payload, mock_response)

    response = await core.track_route(request)  # type: ignore

    assert isinstance(response, JSONResponse)


@pytest.mark.asyncio
async def test_track_route_with_feature_id_camel_case():
    json_payload = {"featureId": "feature_123"}

    mock_response = TrackResponse(
        id="track_123",
        code="success",
        customer_id=DUMMY_CUSTOMER_ID,
        feature_id="feature_123",
    )

    request = _prepare_request(json_payload, mock_response)

    response = await core.track_route(request)  # type: ignore

    assert isinstance(response, JSONResponse)


@pytest.mark.asyncio
async def test_track_route_with_event_name():
    json_payload = {"event_name": "event_123"}

    mock_response = TrackResponse(
        id="track_123",
        code="success",
        customer_id=DUMMY_CUSTOMER_ID,
        event_name="event_123",
    )

    request = _prepare_request(json_payload, mock_response)

    response = await core.track_route(request)  # type: ignore

    assert isinstance(response, JSONResponse)


@pytest.mark.asyncio
async def test_track_route_with_event_name_camel_case():
    json_payload = {"eventName": "event_123"}

    mock_response = TrackResponse(
        id="track_123",
        code="success",
        customer_id=DUMMY_CUSTOMER_ID,
        event_name="event_123",
    )

    request = _prepare_request(json_payload, mock_response)

    response = await core.track_route(request)  # type: ignore

    assert isinstance(response, JSONResponse)


@pytest.mark.asyncio
async def test_track_route_without_feature_id_or_event_name():
    json_payload = {}

    request = _prepare_request(json_payload)

    try:
        await core.track_route(request)  # type: ignore
        assert False, "Should have raised AssertionError"
    except AssertionError as e:
        assert "Either feature_id or event_name must be provided" in str(e)
