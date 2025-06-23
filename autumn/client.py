from __future__ import annotations

from typing import Optional, List, Any, Dict, TYPE_CHECKING

from .customers import Customers
from .features import Features
from .products import Products
from .http import HTTPClient
from .utils import _build_payload
from .types.meta import AttachOption
from .types.response import (
    AttachResponse,
    CheckResponse,
    TrackResponse,
)

if TYPE_CHECKING:
    from .types.features import Feature
    from .types.meta import CustomerData


__all__ = ("Client",)


class Client:
    """
    The main client class for interacting with the Autumn API.

    Example:

    .. code-block:: python

        import autumn

        client = autumn.Client(token="your_api_key")

        # Attach a customer to a product
        client.attach(
            customer_id="john_doe",
            product_id="chat_messages",
        )

    .. note::
        This client should not be used in async contexts. Use :class:`~autumn.aio.client.AsyncClient` instead.
        The :class:`~autumn.aio.client.AsyncClient` class is a *wrapper* around the :class:`~autumn.Client` class that provides async support.
        It works the same, but you must ``await`` your method calls.

        .. code-block:: python

            import asyncio

            from autumn.aio import Client

            async def main():
                client = Client(token="your_api_key")
                await client.attach(customer_id="john_doe", product_id="chat_messages")

            asyncio.run(main())

        The async client requires ``aiohttp`` to be installed. You can install it via: ``pip install aiohttp``.

    Parameters
    ----------
    token: str
        The API key to use for authentication.
    base_url: Optional[str]
        The base URL of the Autumn API. This is useful when you are self-hosting Autumn and need to point to your own instance.

    Attributes
    ----------
    customers: :class:`~autumn.customers.Customers`
        An interface to Autumn's customer API.
    features: :class:`~autumn.features.Features`
        An interface to Autumn's feature API.
    products: :class:`~autumn.products.Products`
        An interface to Autumn's product API.
    """

    def __init__(self, token: str, *, base_url: Optional[str] = None):
        from . import BASE_URL, VERSION

        _base_url = base_url or BASE_URL
        _base_url = _base_url.rstrip("/")

        self.http = HTTPClient(_base_url, VERSION, token)
        self.customers = Customers(self.http)
        self.features = Features(self.http)
        self.products = Products(self.http)

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
        customer_data: Optional[CustomerData] = None,
        free_trial: Optional[bool] = None,
        options: Optional[List[AttachOption]] = None,
    ) -> AttachResponse:
        """Attach a customer to a product.

        |maybecoro|

        Parameters
        ----------
        customer_id: str
            The ID of the customer to attach.
        product_id: Optional[str]
            The ID of the product to attach.
        product_ids: Optional[List[str]]
            The IDs of the products to attach.
        success_url: Optional[str]
            The URL to redirect to after a successful attachment.
        force_checkout: bool
            Whether to force the customer to checkout.
        features: Optional[List[Feature]]
            The features to attach.
        entity_id: Optional[str]
            The ID of the entity to attach.
        customer_data: Optional[CustomerData]
            The customer data to attach.
        free_trial: Optional[bool]
            Whether to attach a free trial.
        options: Optional[List[AttachOption]]
            The options to attach.

        Returns
        -------
        :class:`~autumn.types.response.AttachResponse`
            The response from the API.
        """

        assert product_id is not None or product_ids is not None, (
            "Either product_id or product_ids must be provided"
        )
        assert not (product_id is not None and product_ids is not None), (
            "Only one of product_id or product_ids must be provided"
        )

        payload = _build_payload(locals(), self.attach)
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
        customer_data: Optional[CustomerData] = None,
    ) -> CheckResponse:
        """Check if a customer has access to a product or feature.

        |maybecoro|

        You must pass either ``product_id`` or ``feature_id``. Failure to pass one and **only one** will raise an assertion error.

        Parameters
        ----------
        customer_id: str
            The ID of the customer to check.
        product_id: Optional[str]
            The ID of the product to check.
        feature_id: Optional[str]
            The ID of the feature to check.
        required_balance: Optional[int]
            The required balance to check.
        send_event: bool
            Whether to record a usage event with checking access. The ```required_balance`` field will be used as the usage ``value``.
        with_preview: bool
            If true, the response will include a ``preview`` object, which can be used to display information such as a paywall or upgrade confirmation.
        entity_id: Optional[str]
            If using entity balances (eg, seats), the entity ID to check access for.
        customer_data: Optional[CustomerData]
            Additional customer properties. These will be used if the customer's properties are not already set.

        Returns
        -------
        :class:`~autumn.types.response.CheckResponse`
            The response from the API.
        """

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
        customer_data: Optional[CustomerData] = None,
    ) -> TrackResponse:
        """
        Track a feature usage.

        |maybecoro|

        Parameters
        ----------
        customer_id: str
            The ID of the customer to track.
        feature_id: str
            The ID of the feature to track.
        value: int
            The amount of the feature to deduct.
        entity_id: Optional[str]
            The ID of the entity to track.
        event_name: Optional[str]
            The name of the event to track.
        idempotency_key: Optional[str]
            A unique identifier for the track event. If not provided, the SDK will not generate one - the Autumn API does not expect one.
        properties: Optional[Dict[str, Any]]
            Additional properties to track.
        customer_data: Optional[CustomerData]
            Additional customer properties. These will be used if the customer's properties are not already set.

        Returns
        -------
        :class:`~autumn.types.response.TrackResponse`
            The response from the API.
        """
        payload = _build_payload(locals(), self.track)
        return self.http.request("POST", "/track", TrackResponse, json=payload)
