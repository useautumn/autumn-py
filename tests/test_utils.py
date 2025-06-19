import pytest

from autumn.types.customers import CustomerFeature, ProductItemInterval
from autumn.customers import Customers
from autumn.error import AutumnValidationError, AutumnHTTPError
from autumn.utils import _build_model, _build_payload, _decompose_value, _check_response


def test_decompose_value_singular():
    feature = CustomerFeature(
        id="mock_id",
        name="John Doe",
        unlimited=False,
        interval=ProductItemInterval.HOUR,
    )
    decomposed_feature = {
        "id": "mock_id",
        "name": "John Doe",
        "unlimited": False,
        "interval": "hour",
        "balance": None,
        "usage": None,
        "included_usage": None,
        "next_reset_at": None,
        "breakdown": None,
    }

    assert _decompose_value(feature) == decomposed_feature


def test_decompose_value_recursive():
    feature = CustomerFeature(
        id="mock_id",
        name="John Doe",
        unlimited=False,
        interval=ProductItemInterval.HOUR,
    )
    decomposed_feature = {
        "id": "mock_id",
        "name": "John Doe",
        "unlimited": False,
        "interval": "hour",
        "balance": None,
        "usage": None,
        "included_usage": None,
        "next_reset_at": None,
        "breakdown": None,
    }

    features = [feature] * 50
    decomposed_features = [decomposed_feature] * 50

    assert _decompose_value(features) == decomposed_features


def test_build_payload():
    mock_scope = {
        "self": None,
        "id": "mock_customer_id",
        "email": "johndoe@example.com",
        "name": "John Doe",
        **locals(),
    }
    expected_payload = {
        "id": "mock_customer_id",
        "email": "johndoe@example.com",
        "name": "John Doe",
    }

    assert _build_payload(mock_scope, Customers.create) == expected_payload


def test_model_build_exc():
    bad_data = {
        "id": "mock_id",
        "name": "John Doe",
        "unlimited": False,
        "interval": "chocolate",
        "balance": "",
        "usage": None,
        "included_usage": None,
        "next_reset_at": None,
        "breakdown": None,
    }

    with pytest.raises(AutumnValidationError):
        _build_model(CustomerFeature, bad_data)


def test_check_response():
    data = {"mock": "data"}

    for code in range(200, 299 + 1):
        _check_response(code, data)

    with pytest.raises(AutumnHTTPError):
        _check_response(300, data)

    with pytest.raises(AutumnHTTPError):
        _check_response(301, data)
