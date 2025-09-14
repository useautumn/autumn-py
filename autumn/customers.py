from __future__ import annotations

from typing import (
    TYPE_CHECKING,
    Any,
    Coroutine,
    Dict,
    Generic,
    List,
    Literal,
    Optional,
    TypeVar,
    Union,
    overload,
)

from .models.customers import Customer
from .models.meta import Empty
from .models.response import (
    BillingPortalResponse,
    ListCustomerResponse,
    PricingTableResponse,
)
from .utils import _build_payload

if TYPE_CHECKING:
    from .aio.http import AsyncHTTPClient
    from .http import HTTPClient

T_HttpClient = TypeVar("T_HttpClient", "AsyncHTTPClient", "HTTPClient")

__all__ = ("Customers",)


class Customers(Generic[T_HttpClient]):
    """An interface to Autumn's customer API.

    .. warning::
        This class is not intended for public use. It is used internally by the :class:`autumn.Client` class.
        Do not initialize this class directly.
    """

    def __init__(self, http: T_HttpClient):
        self._http = http

    @overload
    def get(
        self: "Customers[HTTPClient]",
        customer_id: str,
        expand: Optional[
            List[
                Literal[
                    "invoices",
                    "rewards",
                    "trials_used",
                    "entities",
                    "referrals",
                    "payment_method",
                ]
            ]
        ] = None,
    ) -> Customer: ...

    @overload
    def get(
        self: "Customers[AsyncHTTPClient]",
        customer_id: str,
        expand: Optional[
            List[
                Literal[
                    "invoices",
                    "rewards",
                    "trials_used",
                    "entities",
                    "referrals",
                    "payment_method",
                ]
            ]
        ] = None,
    ) -> Coroutine[Any, Any, Customer]: ...

    def get(
        self,
        customer_id: str,
        expand: Optional[
            List[
                Literal[
                    "invoices",
                    "rewards",
                    "trials_used",
                    "entities",
                    "referrals",
                    "payment_method",
                ]
            ]
        ] = None,
    ) -> Union[Customer, Coroutine[Any, Any, Customer]]:
        """Get a customer by their ID.

        |maybecoro|

        Parameters
        ----------
        customer_id: str
            The ID of the customer to get.
        expand: Optional[List[Literal["invoices", "rewards", "trials_used", "entities", "referrals", "payment_method"]]]
            Additional fields to expand in the response.

        Returns
        -------
        :class:`~autumn.models.customers.Customer`
            The customer.
        """
        params = {}
        if expand is not None:
            params["expand"] = expand
        return self._http.request(
            "GET", f"/customers/{customer_id}", Customer, params=params
        )

    @overload
    def list(
        self: "Customers[HTTPClient]", *, limit: int = 10, offset: int = 0
    ) -> ListCustomerResponse: ...

    @overload
    def list(
        self: "Customers[AsyncHTTPClient]", *, limit: int = 10, offset: int = 0
    ) -> Coroutine[Any, Any, ListCustomerResponse]: ...

    def list(
        self, *, limit: int = 10, offset: int = 0
    ) -> Union[
        ListCustomerResponse, Coroutine[Any, Any, ListCustomerResponse]
    ]:
        params = {"limit": limit, "offset": offset}
        return self._http.request(
            "GET", "/customers", ListCustomerResponse, params=params
        )

    @overload
    def create(
        self: "Customers[HTTPClient]",
        id: str,
        *,
        email: Optional[str] = None,
        name: Optional[str] = None,
        stripe_id: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Customer: ...

    @overload
    def create(
        self: "Customers[AsyncHTTPClient]",
        id: str,
        *,
        email: Optional[str] = None,
        name: Optional[str] = None,
        stripe_id: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Coroutine[Any, Any, Customer]: ...

    def create(
        self,
        id: str,
        *,
        email: Optional[str] = None,
        name: Optional[str] = None,
        stripe_id: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Union[Customer, Coroutine[Any, Any, Customer]]:
        """Create a new customer.

        |maybecoro|

        Parameters
        ----------
        id: str
            The ID of the customer to create.
        email: Optional[str]
            The customer's email address.
        name: Optional[str]
            The customer's name.
        stripe_id: Optional[str]
            The customer's Stripe ID. This can be a new or existing ID.
        metadata: Optional[Dict[str, Any]]
            Additional metadata to attach to the customer.

        Returns
        -------
        :class:`~autumn.models.customers.Customer`
            The created customer.
        """
        payload = _build_payload(locals(), Customers.create)
        return self._http.request("POST", "/customers", Customer, json=payload)

    @overload
    def update(
        self: "Customers[HTTPClient]",
        customer_id: str,
        *,
        name: Optional[str] = None,
        email: Optional[str] = None,
        fingerprint: Optional[str] = None,
    ) -> Customer: ...

    @overload
    def update(
        self: "Customers[AsyncHTTPClient]",
        customer_id: str,
        *,
        name: Optional[str] = None,
        email: Optional[str] = None,
        fingerprint: Optional[str] = None,
    ) -> Coroutine[Any, Any, Customer]: ...

    def update(
        self,
        customer_id: str,
        *,
        name: Optional[str] = None,
        email: Optional[str] = None,
        fingerprint: Optional[str] = None,
    ) -> Union[Customer, Coroutine[Any, Any, Customer]]:
        """Update a customer.

        |maybecoro|

        Parameters
        ----------
        customer_id: str
            The ID of the customer to update.
        name: Optional[str]
            The customer's new name.
        email: Optional[str]
            The customer's new email address.
        fingerprint: Optional[str]
            The customer's new fingerprint.

        Returns
        -------
        :class:`~autumn.models.customers.Customer`
            The updated customer.
        """
        payload = _build_payload(
            locals(), Customers.update, ignore={"customer_id"}
        )
        return self._http.request(
            "POST", f"/customers/{customer_id}", Customer, json=payload
        )

    @overload
    def delete(self: "Customers[HTTPClient]", customer_id: str) -> Empty: ...

    @overload
    def delete(
        self: "Customers[AsyncHTTPClient]", customer_id: str
    ) -> Coroutine[Any, Any, Empty]: ...

    def delete(
        self, customer_id: str
    ) -> Union[Empty, Coroutine[Any, Any, Empty]]:
        """Delete a customer.

        Parameters
        ----------
        customer_id: str
            The ID of the customer to delete.

        Returns
        -------
        :class:`~autumn.models.customers.Empty`
            An empty response.

        |maybecoro|
        """
        return self._http.request("DELETE", f"/customers/{customer_id}", Empty)

    @overload
    def get_billing_portal(
        self: "Customers[HTTPClient]",
        customer_id: str,
        *,
        return_url: Optional[str] = None,
    ) -> BillingPortalResponse: ...

    @overload
    def get_billing_portal(
        self: "Customers[AsyncHTTPClient]",
        customer_id: str,
        *,
        return_url: Optional[str] = None,
    ) -> Coroutine[Any, Any, BillingPortalResponse]: ...

    def get_billing_portal(
        self,
        customer_id: str,
        *,
        return_url: Optional[str] = None,
    ) -> Union[
        BillingPortalResponse, Coroutine[Any, Any, BillingPortalResponse]
    ]:
        """Get a billing portal URL for a customer.

        |maybecoro|

        Parameters
        ----------
        customer_id: str
            The ID of the customer to get a billing portal URL for.
        return_url: Optional[str]
            The URL to return to after the customer has completed the billing portal.

        Returns
        -------
        :class:`~autumn.models.response.BillingPortalResponse`
            The billing portal URL.
        """
        payload = _build_payload(
            locals(),
            Customers.get_billing_portal,
            ignore={"customer_id"},
        )
        return self._http.request(
            "POST",
            f"/customers/{customer_id}/billing_portal",
            BillingPortalResponse,
            json=payload,
        )

    @overload
    def pricing_table(
        self: "Customers[HTTPClient]", customer_id: str
    ) -> PricingTableResponse: ...

    @overload
    def pricing_table(
        self: "Customers[AsyncHTTPClient]", customer_id: str
    ) -> Coroutine[Any, Any, PricingTableResponse]: ...

    def pricing_table(
        self, customer_id: str
    ) -> Union[
        PricingTableResponse, Coroutine[Any, Any, PricingTableResponse]
    ]:
        """Get a pricing table for a customer.

        |maybecoro|

        Parameters
        ----------
        customer_id: str
            The ID of the customer to get a pricing table for.

        Returns
        -------
        :class:`~autumn.models.response.PricingTableResponse`
            The pricing table.
        """
        params = {"customer_id": customer_id}
        return self._http.request(
            "GET",
            "/components/pricing_table",
            PricingTableResponse,
            params=params,
        )
