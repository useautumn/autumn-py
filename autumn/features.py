from __future__ import annotations

from typing import (
    TYPE_CHECKING,
    Any,
    Coroutine,
    Generic,
    List,
    TypeVar,
    Union,
    overload,
)

from .models.balance import Balance
from .models.meta import Empty
from .utils import _build_payload

if TYPE_CHECKING:
    from .aio.http import AsyncHTTPClient
    from .http import HTTPClient

T_HttpClient = TypeVar("T_HttpClient", "AsyncHTTPClient", "HTTPClient")


class Features(Generic[T_HttpClient]):
    """An interface to Autumn's feature API.

    .. warning::
        This class is not intended for public use. It is used internally by the :class:`autumn.Client` class.
        Do not initialize this class directly.
    """

    def __init__(self, http: T_HttpClient):
        self._http = http

    @overload
    def set_usage(
        self: "Features[HTTPClient]", customer_id: str, feature_id: str, value: int
    ) -> Empty: ...

    @overload
    def set_usage(
        self: "Features[AsyncHTTPClient]", customer_id: str, feature_id: str, value: int
    ) -> Coroutine[Any, Any, Empty]: ...

    def set_usage(
        self, customer_id: str, feature_id: str, value: int
    ) -> Union[Empty, Coroutine[Any, Any, Empty]]:
        """Set the usage of a feature for a customer.

        |maybecoro|

        Parameters
        ----------
        customer_id: str
            The ID of the customer to set the usage for.
        feature_id: str
            The ID of the feature to set the usage for.
        value: int
            The amount the usage should be updated to.

        Returns
        -------
        :class:`~autumn.models.response.Empty`
            This is a placeholder type. Treat it as :class:`None`.
        """
        payload = _build_payload(locals(), Features.set_usage, ignore={"customer_id"})  # type: ignore
        return self._http.request(
            "POST",
            f"/customers/{customer_id}/balances",
            Empty,
            json=payload,
        )

    @overload
    def set_balances(
        self: "Features[HTTPClient]",
        customer_id: str,
        balances: List[Balance],
    ) -> Empty: ...

    @overload
    def set_balances(
        self: "Features[AsyncHTTPClient]",
        customer_id: str,
        balances: List[Balance],
    ) -> Coroutine[Any, Any, Empty]: ...

    def set_balances(
        self, customer_id: str, balances: List[Balance]
    ) -> Union[Empty, Coroutine[Any, Any, Empty]]:
        """Set the balances of a customer.

        |maybecoro|

        Parameters
        ----------
        customer_id: str
            The ID of the customer to set the balances for.
        balances: List[:class:`~autumn.models.balance.Balance`]
            The balances to set for the customer.

        Returns
        -------
        :class:`~autumn.models.response.Empty`
            This is a placeholder type. Treat it as :class:`None`.
        """

        payload = _build_payload(locals(), Features.set_balances, ignore={"customer_id"})  # type: ignore
        return self._http.request(
            "POST", f"/customers/{customer_id}/balances", Empty, json=payload
        )
