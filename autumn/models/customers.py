from __future__ import annotations

from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel

from .meta import AppEnv
from .products import ProductItemInterval

__all__ = (
    "ProductStatus",
    "CustomerInvoice",
    "CustomerFeature",
    "CustomerProduct",
    "Customer",
    "PriceInfo",
    "ItemInfo",
    "GetPricingTableParams",
    "PricingTableProduct",
)


class ProductStatus(str, Enum):
    ACTIVE = "active"
    EXPIRED = "expired"
    TRIALING = "trialing"
    SCHEDULED = "scheduled"


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


class Customer(BaseModel):
    id: Optional[str] = None
    created_at: int
    name: Optional[str] = None
    email: Optional[str] = None
    fingerprint: Optional[str] = None
    stripe_id: Optional[str] = None
    env: AppEnv
    metadata: Dict[str, Any]
    products: List[CustomerProduct]
    features: Dict[str, CustomerFeature]
    invoices: Optional[List[CustomerInvoice]] = None


class PriceInfo(BaseModel):
    primaryText: str
    secondaryText: Optional[str] = None


class ItemInfo(BaseModel):
    primaryText: str
    secondaryText: Optional[str] = None


class GetPricingTableParams(BaseModel):
    customer_id: Optional[str] = None


class PricingTableProduct(BaseModel):
    id: str
    name: str
    buttonText: str
    price: PriceInfo
    items: List[ItemInfo]
