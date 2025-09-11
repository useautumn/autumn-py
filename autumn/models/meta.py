from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING, Optional

from pydantic import BaseModel, ConfigDict

from .products import ProductItem

if TYPE_CHECKING:
    from typing import Any, Dict

    Metadata = Dict[str, Any]

__all__ = ("Empty", "FeatureOptions", "ProductOptions", "CustomerData")


class Empty(BaseModel): ...


class FeatureOptions(BaseModel):
    feature_id: str
    quantity: int


class ProductOptions(BaseModel):
    product_id: str
    quantity: Optional[int] = None


class CustomerData(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    fingerprint: Optional[str] = None


class AttachProductOptions(BaseModel):
    product_id: str
    quantity: Optional[int] = None


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
