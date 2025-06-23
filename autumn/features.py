from __future__ import annotations

from typing import (
    List,
    Any,
    TypeVar,
    Generic,
    overload,
    Coroutine,
    Union,
    Optional,
    TYPE_CHECKING,
)

from .types.balance import Balance
from .types.meta import Empty
from .types.features import Entity
from .utils import _build_payload

if TYPE_CHECKING:
    from .http import HTTPClient
    from .aio.http import AsyncHTTPClient


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
        :class:`~autumn.types.response.Empty`
            This is a placeholder type. Treat it as :class:`None`.
        """
        payload = _build_payload(locals(), self.set_usage, ignore={"customer_id"})  # type: ignore
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
        balances: List[:class:`~autumn.types.balance.Balance`]
            The balances to set for the customer.

        Returns
        -------
        :class:`~autumn.types.response.Empty`
            This is a placeholder type. Treat it as :class:`None`.
        """

        payload = _build_payload(locals(), self.set_balances, ignore={"customer_id"})  # type: ignore
        return self._http.request(
            "POST", f"/customers/{customer_id}/balances", Empty, json=payload
        )

    @overload
    def create_entity(
        self: "Features[HTTPClient]",
        customer_id: str,
        id: str,
        feature_id: str,
        name: str,
    ) -> Empty: ...

    @overload
    def create_entity(
        self: "Features[AsyncHTTPClient]",
        customer_id: str,
        id: str,
        feature_id: str,
        name: str,
    ) -> Coroutine[Any, Any, Empty]: ...

    def create_entity(
        self, customer_id: str, id: str, feature_id: str, name: str
    ) -> Union[Empty, Coroutine[Any, Any, Empty]]:
        """Create an entity for a customer.

        |maybecoro|

        Parameters
        ----------
        customer_id: str
            The ID of the customer to create the entity for.
        id: str
            The ID of the entity to create.
        feature_id: str
            The ID of the feature to create the entity for.
        name: str
            The name of the entity to create.

        Returns
        -------
        :class:`~autumn.types.response.Empty`
            This is a placeholder type. Treat it as :class:`None`.
        """

        payload = _build_payload(locals(), self.create_entity, ignore={"customer_id"})  # type: ignore
        return self._http.request(
            "POST", f"/customers/{customer_id}/entities", Empty, json=payload
        )

    @overload
    def get_entity(
        self: "Features[HTTPClient]",
        customer_id: str,
        entity_id: str,
        expand: Optional[List[str]] = None,
    ) -> Entity: ...

    @overload
    def get_entity(
        self: "Features[AsyncHTTPClient]",
        customer_id: str,
        entity_id: str,
        expand: Optional[List[str]] = None,
    ) -> Coroutine[Any, Any, Entity]: ...

    def get_entity(
        self, customer_id: str, entity_id: str, expand: Optional[List[str]] = None
    ) -> Union[Entity, Coroutine[Any, Any, Entity]]:
        """Get an entity

        |maybecoro|

        This method is undocumented and will remain undocumented until the official Autumn docs document this route.

        """
        params = {"expand": expand}
        return self._http.request(
            "GET",
            f"/customers/{customer_id}/entities/{entity_id}",
            Entity,
            params=params,
        )

    @overload
    def delete_entity(
        self: "Features[HTTPClient]",
        customer_id: str,
        entity_id: str,
    ) -> Empty: ...

    @overload
    def delete_entity(
        self: "Features[AsyncHTTPClient]",
        customer_id: str,
        entity_id: str,
    ) -> Coroutine[Any, Any, Empty]: ...

    def delete_entity(
        self, customer_id: str, entity_id: str
    ) -> Union[Empty, Coroutine[Any, Any, Empty]]:
        """Delete an entity for a customer.

        |maybecoro|

        Parameters
        ----------
        customer_id: str
            The ID of the customer to delete the entity for.
        entity_id: str
            The ID of the entity to delete.

        Returns
        -------
        :class:`~autumn.types.response.Empty`
            This is a placeholder type. Treat it as :class:`None`.
        """

        return self._http.request(
            "DELETE", f"/customers/{customer_id}/entities/{entity_id}", Empty
        )
