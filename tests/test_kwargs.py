import pytest

from autumn.utils import _build_payload as _build_kwargs


def _temp_method(customer_id: str, feature_id: str, *, range: str):
    pass

def test_build_kwargs():
    json_data = {
        "open_in_new_tab": True,
        "openInNewTab": True,
        "customer_id": "cus_id",
        "feature_id": "feature_id",
        "range": "24h",
    }

    kwargs = _build_kwargs(json_data, _temp_method)
    
    _temp_method(**kwargs)