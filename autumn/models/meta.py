from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING, Optional

from pydantic import BaseModel, ConfigDict

from .products import ProductItem

if TYPE_CHECKING:
    from typing import Dict, Any

    Metadata = Dict[str, Any]


__all__ = (
    "Empty",
    "AppEnv",
    "AttachOption",
    "CustomerData",
)


class Empty(BaseModel): ...


class AppEnv(str, Enum):
    PRODUCTION = "production"
    SANDBOX = "sandbox"
    LIVE = "live"


class AttachOption(BaseModel):
    feature_id: str
    quantity: int


class CustomerData(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    fingerprint: Optional[str] = None


class CheckoutLine(BaseModel):
    description: str
    amount: int
    item: ProductItem


class Cycle(BaseModel):
    starts_at: int
    total: float


class QueryDP(BaseModel):
    period: int

    model_config = ConfigDict(extra="allow")

    def get_usage(self, key: str) -> Optional[int]:
        if self.__pydantic_extra__ is None:
            return None

        return self.__pydantic_extra__.get(key)
