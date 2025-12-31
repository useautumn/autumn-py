from __future__ import annotations

from enum import Enum
from typing import Any, Dict, List, Literal, Optional

from pydantic import BaseModel

from .products import ProductItemInterval

__all__ = (
    "ProductStatus",
    "FeatureType",
    "CustomerInvoice",
    "CustomerFeature",
    "CustomerProduct",
)


class ProductStatus(str, Enum):
    ACTIVE = "active"
    EXPIRED = "expired"
    TRIALING = "trialing"
    SCHEDULED = "scheduled"


class FeatureType(str, Enum):
    STATIC = "static"
    CONTINUOUS_USE = "continuous_use"
    SINGLE_USE = "single_use"
    BOOLEAN = "boolean"


class CustomerInvoice(BaseModel):
    product_ids: List[str]
    stripe_id: str
    status: str
    total: float
    currency: str
    created_at: int


class CustomerFeature(BaseModel):
    id: str
    name: str
    unlimited: Optional[bool] = None
    type: Optional[FeatureType] = None
    interval: Optional[ProductItemInterval] = None
    balance: Optional[float] = None
    usage: Optional[float] = None
    included_usage: Optional[float] = None
    next_reset_at: Optional[int] = None
    breakdown: Optional[List[Dict[str, Any]]] = None


class CustomerProduct(BaseModel):
    id: str
    name: Optional[str] = None
    group: Optional[str] = None
    status: ProductStatus
    started_at: int
    canceled_at: Optional[int] = None
    subscription_ids: Optional[List[str]] = None
    current_period_start: Optional[int] = None
    current_period_end: Optional[int] = None
    quantity: Optional[int] = None


class CustomerDiscount(BaseModel):
    id: str
    name: str
    type: Literal["percentage_discount", "fixed_discount"]
    discount_value: float
    duration_type: Literal["one_off", "months", "forever"]
    duration_value: Optional[int] = None
    currency: Optional[str] = None
    start: Optional[int] = None
    end: Optional[int] = None
    subscription_id: Optional[str] = None
    total_discount_amount: Optional[float] = None


class UpcomingInvoiceLine(BaseModel):
    product_id: Optional[str] = None
    description: str
    amount: float


class UpcomingInvoice(BaseModel):
    lines: List[UpcomingInvoiceLine]
    discounts: List[CustomerDiscount]
    subtotal: float
    total: float
    currency: str
