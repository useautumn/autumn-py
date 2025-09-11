from __future__ import annotations

from typing import (
    TYPE_CHECKING,
    Any,
    Coroutine,
    Dict,
    Generic,
    List,
    Optional,
    TypeVar,
    Union,
    overload,
)

from .models.entities import Entity
from .models.meta import Empty
from .models.response import TransferProductResponse
from .utils import _build_payload

if TYPE_CHECKING:
    from .aio.http import AsyncHTTPClient
    from .http import HTTPClient

T_HttpClient = TypeVar("T_HttpClient", "AsyncHTTPClient", "HTTPClient")

__all__ = ("Entities",)


class Entities(Generic[T_HttpClient]):
    """An interface to Autumn's entities API.

    .. warning::
        This class is not intended for public use. It is used internally by the :class:`autumn.Client` class.
        Do not initialize this class directly.
    """

    def __init__(self, http: T_HttpClient):
        self._http = http

    @overload
    def get(
        self: "Entities[HTTPClient]",
        customer_id: str,
        entity_id: str,
        expand: Optional[List[str]] = None,
    ) -> Entity: ...

    @overload
    def get(
        self: "Entities[AsyncHTTPClient]",
        customer_id: str,
        entity_id: str,
        expand: Optional[List[str]] = None,
    ) -> Coroutine[Any, Any, Entity]: ...

    def get(
        self, customer_id: str, entity_id: str, expand: Optional[List[str]] = None
    ) -> Union[Entity, Coroutine[Any, Any, Entity]]:
        """Get an entity by their ID.

        |maybecoro|

        Parameters
        ----------
        customer_id: str
            The ID of the customer to get.
        entity_id: str
            The ID of the entity to get.
        expand: Optional[List[str]]
            Additional fields to expand in the response.

        Returns
        -------
        :class:`~autumn.models.entities.Entity`
            The entity.
        """
        params = {}
        if expand is not None:
            params["expand"] = expand
        return self._http.request(
            "GET",
            f"/customers/{customer_id}/entities/{entity_id}",
            Entity,
            params=params,
        )

    @overload
    def create(
        self: "Entities[HTTPClient]",
        customer_id: str,
        id: str,
        feature_id: str,
        name: str,
    ) -> Entity: ...

    @overload
    def create(
        self: "Entities[AsyncHTTPClient]",
        customer_id: str,
        id: str,
        feature_id: str,
        name: str,
    ) -> Coroutine[Any, Any, Entity]: ...

    def create(
        self, customer_id: str, id: str, feature_id: str, name: str
    ) -> Union[Entity, Coroutine[Any, Any, Entity]]:
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
        :class:`~autumn.models.entities.Entity`
            The created entity.
        """

        payload = _build_payload(locals(), Entities.create, ignore={"customer_id"})
        return self._http.request(
            "POST", f"/customers/{customer_id}/entities", Entity, json=payload
        )

    @overload
    def delete(
        self: "Entities[HTTPClient]",
        customer_id: str,
        entity_id: str,
    ) -> Empty: ...

    @overload
    def delete(
        self: "Entities[AsyncHTTPClient]",
        customer_id: str,
        entity_id: str,
    ) -> Coroutine[Any, Any, Empty]: ...

    def delete(
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
        :class:`~autumn.models.meta.Empty`
            This is a placeholder type. Treat it as :class:`None`.
        """

        return self._http.request(
            "DELETE", f"/customers/{customer_id}/entities/{entity_id}", Empty
        )

    @overload
    def transfer(
        self: "Entities[HTTPClient]",
        customer_id: str,
        to_entity_id: str,
        product_id: str,
        from_entity_id: Optional[str] = None,
    ) -> TransferProductResponse: ...

    @overload
    def transfer(
        self: "Entities[AsyncHTTPClient]",
        customer_id: str,
        to_entity_id: str,
        product_id: str,
        from_entity_id: Optional[str] = None,
    ) -> Coroutine[Any, Any, TransferProductResponse]: ...

    def transfer(
        self,
        customer_id: str,
        to_entity_id: str,
        product_id: str,
        from_entity_id: Optional[str] = None,
    ) -> Union[TransferProductResponse, Coroutine[Any, Any, TransferProductResponse]]:
        """Transfer a product from one entity to another.

        |maybecoro|

        Parameters
        ----------
        customer_id: str
            The ID of the customer who owns the entities.
        to_entity_id: str
            The ID of the entity to transfer the product to.
        product_id: str
            The ID of the product to transfer.
        from_entity_id: Optional[str]
            The ID of the entity to transfer the product from. If not provided,
            transfers from the customer's general balance.

        Returns
        -------
        :class:`~autumn.models.entities.TransferProductResult`
            The result of the transfer operation.
        """

        payload = _build_payload(locals(), Entities.transfer, ignore={"customer_id"})
        return self._http.request(
            "POST",
            f"/customers/{customer_id}/transfer",
            TransferProductResponse,
            json=payload,
        )
