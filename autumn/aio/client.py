from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from ..client import Client
from ..customers import Customers
from ..entities import Entities
from ..error import AutumnError
from ..features import Features
from ..products import Products
from .http import AsyncHTTPClient

try:
    import aiohttp
except ImportError:
    raise AutumnError(
        "aiohttp is not installed. Please install it with `pip install aiohttp`",
        "missing_dependency",
    )

if TYPE_CHECKING:
    from typing_extensions import Self

    from .stubs import (
        AttachParams,
        CancelParams,
        CheckoutParams,
        CheckParams,
        QueryParams,
        TrackParams,
    )

__all__ = ("AsyncClient",)


class AsyncClient(Client):
    """
    The ``async`` client class for interacting with the Autumn API.

    This class is also exposed as ``autumn.Autumn``.

    The ``AsyncClient`` automatically retries requests up to 5 times, exponentially backing off between attempts.

    Note that session creation is lazy. This means that the ``AsyncClient`` will not attempt to create a session until the first request is made.

    Parameters
    ----------
    token: str
        The API key to use for authentication.
    base_url: Optional[str]
        The base URL of the Autumn API. This is useful when you are self-hosting Autumn and need to point to your own instance.
    max_retries: int
        The maximum number of retries to attempt for failed requests.
    session: Optional[:class:`~aiohttp.ClientSession`]
        The session to use for requests. If not provided, a new session will be created **lazily**.

    Attributes
    ----------
    customers: :class:`~autumn.customers.Customers`
        An interface to Autumn's customer API.
    features: :class:`~autumn.features.Features`
        An interface to Autumn's feature API.
    products: :class:`~autumn.products.Products`
        An interface to Autumn's product API.
    entities: :class:`~autumn.entities.Entities`
        An interface to Autumn's entities API.

    """

    attach: AttachParams  # type: ignore
    check: CheckParams  # type: ignore
    track: TrackParams  # type: ignore
    checkout: CheckoutParams  # type: ignore
    query: QueryParams  # type: ignore
    cancel: CancelParams  # type: ignore

    def __init__(
        self,
        token: str,
        *,
        base_url: Optional[str] = None,
        max_retries: int = 5,
        session: Optional[aiohttp.ClientSession] = None,
    ) -> None:
        from .. import BASE_URL, VERSION

        _base_url = base_url or BASE_URL
        _base_url = _base_url.rstrip("/")

        attempts = max_retries + 1
        self.http = AsyncHTTPClient(
            _base_url,
            VERSION,
            token,
            attempts=attempts,
            session=session,
        )
        self.customers = Customers(self.http)
        self.features = Features(self.http)
        self.products = Products(self.http)
        self.entities = Entities(self.http)

    async def __aenter__(self) -> Self:
        return self

    async def __aexit__(self, _exc_type, _exc, _tb):
        await self.close()

    async def close(self):
        await self.http.close()
