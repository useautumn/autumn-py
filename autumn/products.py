from __future__ import annotations

from typing import (
    List,
    Any,
    Union,
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
    """An interface to Autumn's product API.

    .. warning::
        This class is not intended for public use. It is used internally by the :class:`autumn.Client` class.
        Do not initialize this class directly.

    Example:

    .. code-block:: python

        import autumn

        client = autumn.Client(token="your_api_key")

        product = client.products.create(
            id="chat_messages",
            name="Chat Messages"
        )

        print(product.name) # Chat Messages

    """

    def __init__(self, http: T_HttpClient):
        self._http = http

    @overload
    def create(
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
    def create(
        self: "Products[AsyncHTTPClient]",
        id: str,
        *,
        name: str,
        is_add_on: bool = False,
        is_default: bool = False,
        items: Optional[List[ProductItem]] = None,
        free_trial: Optional[FreeTrial] = None,
    ) -> Coroutine[Any, Any, CreateProductResponse]: ...

    def create(
        self,
        id: str,
        *,
        name: str,
        is_add_on: bool = False,
        is_default: bool = False,
        items: Optional[List[ProductItem]] = None,
        free_trial: Optional[FreeTrial] = None,
    ) -> Union[CreateProductResponse, Coroutine[Any, Any, CreateProductResponse]]:
        """Create a new product.

        |maybecoro|

        Parameters
        ----------
        id: str
            The ID of the product.
        name: str
            The name of the product.
        is_add_on: bool
            Whether the product is an add-on.
        is_default: bool
            Whether the product is a default product.
        items: Optional[List[ProductItem]]
            The items of the product.
        free_trial: Optional[FreeTrial]
            The free trial configuration of the product.

        Returns
        -------
        :class:`~autumn.types.response.CreateProductResponse`
            The response from the API.
        """
        payload = _build_payload(locals(), self.create)  # type: ignore
        return self._http.request(
            "POST", "/products", CreateProductResponse, json=payload
        )

    @overload
    def get(
        self: "Products[HTTPClient]",
        id: str,
    ) -> GetProductResponse: ...

    @overload
    def get(
        self: "Products[AsyncHTTPClient]",
        id: str,
    ) -> Coroutine[Any, Any, GetProductResponse]: ...

    def get(
        self, id: str
    ) -> Union[GetProductResponse, Coroutine[Any, Any, GetProductResponse]]:
        """Get a product by its ID.

        |maybecoro|

        Parameters
        ----------
        id: str
            The ID of the product to get.

        Returns
        -------
        :class:`~autumn.types.response.GetProductResponse`
            The response from the API.
        """
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
    ) -> Union[ReferralCodeResponse, Coroutine[Any, Any, ReferralCodeResponse]]:
        """Get a referral code for a customer.

        |maybecoro|

        Parameters
        ----------
        customer_id: str
            The ID of the customer to get a referral code for.
        program_id: str
            The ID of the program to get a referral code for.

        Returns
        -------
        :class:`~autumn.types.response.ReferralCodeResponse`
            The response from the API.
        """

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
    ) -> Union[ReferralRedeemResponse, Coroutine[Any, Any, ReferralRedeemResponse]]:
        """Redeem a referral code for a customer.

        |maybecoro|

        Parameters
        ----------
        code: str
            The code to redeem.
        customer_id: str
            The ID of the customer to redeem the code for.
        reward_id: str
            The ID of the reward to redeem.

        Returns
        -------
        :class:`~autumn.types.response.ReferralRedeemResponse`
            The response from the API.
        """
        payload = _build_payload(locals(), self.redeem_referral_code)  # type: ignore
        return self._http.request(
            "POST",
            "/referrals/redeem",
            ReferralRedeemResponse,
            json=payload,
        )

    @overload
    def cancel(
        self: "Products[HTTPClient]",
        customer_id: str,
        product_id: str,
        *,
        entity_id: Optional[str] = None,
        cancel_immediately: bool = False
    ) -> ProductCancelResponse: ...

    @overload
    def cancel(
        self: "Products[AsyncHTTPClient]",
        customer_id: str,
        product_id: str,
        *,
        entity_id: Optional[str] = None,
        cancel_immediately: bool = False
    ) -> Coroutine[Any, Any, ProductCancelResponse]: ...

    def cancel(
        self,
        customer_id: str,
        product_id: str,
        *,
        entity_id: Optional[str] = None,
        cancel_immediately: bool = False
    ) -> Union[ProductCancelResponse, Coroutine[Any, Any, ProductCancelResponse]]:
        """Cancel a product for a customer.

        |maybecoro|

        Parameters
        ----------
        customer_id: str
            The ID of the customer to cancel the product for.
        product_id: str
            The ID of the product to cancel.
        entity_id: Optional[str]
            The ID of the entity to cancel the product for.
        cancel_immediately: bool
            Whether to cancel the product immediately. If false, the product will be cancelled at the end of the billing cycle.

        Returns
        -------
        :class:`~autumn.types.response.ProductCancelResponse`
            The response from the API.
        """
        payload = _build_payload(locals(), self.cancel_product)  # type: ignore
        return self._http.request(
            "POST",
            "/cancel",
            ProductCancelResponse,
            json=payload,
        )
