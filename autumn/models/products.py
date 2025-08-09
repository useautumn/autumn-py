from enum import Enum
from typing import Literal, List, Optional, Union

from pydantic import BaseModel

__all__ = (
    "FreeTrialDuration",
    "UsageModel",
    "ProductItemInterval",
    "PriceCurrencyPair",
    "PriceTier",
    "ProductItem",
    "FreeTrial",
    "Product",
)


class FreeTrialDuration(str, Enum):
    DAY = "day"


class UsageModel(str, Enum):
    PREPAID = "prepaid"
    PAY_PER_USE = "pay_per_use"


class ProductItemInterval(str, Enum):
    MINUTE = "minute"
    HOUR = "hour"
    DAY = "day"
    WEEK = "week"
    MONTH = "month"
    QUARTER = "quarter"
    SEMI_ANNUAL = "semi_annual"
    YEAR = "year"
    MULTIPLE = "multiple"
    LIFETIME = "lifetime"


class PriceCurrencyPair(BaseModel):
    price: float
    currency: str


class PriceTier(BaseModel):
    to: float
    amount: Union[float, str]  # Can be a number or "inf"


class ProductItem(BaseModel):
    feature_id: Optional[str] = None
    included_usage: Optional[Union[float, str]] = None  # Infinite is "inf"
    interval: Optional[ProductItemInterval] = None
    usage_model: Optional[UsageModel] = None
    price: Optional[float] = None
    billing_units: Optional[float] = None
    entity_feature_id: Optional[str] = None
    reset_usage_on_billing: Optional[bool] = None
    reset_usage_when_enabled: Optional[bool] = None


class FreeTrial(BaseModel):
    duration: FreeTrialDuration
    length: float
    unique_fingerprint: bool


ProductScenario = Literal["scheduled", "active", "new", "renew", "upgrade", "downgrade", "cancel"]

class Product(BaseModel):
    created_at: float
    id: str
    name: Optional[str] = None
    env: Literal["sandbox", "live"]
    is_add_on: bool
    is_default: bool
    group: Optional[str] = None
    version: float
    items: List[ProductItem]
    free_trial: Optional[FreeTrial] = None
    scenario: Optional[ProductScenario] = None
    base_variant_id: Optional[str] = None


class ProductPreview(BaseModel):
    title: str
    message: str
    scenario: Literal["upgrade", "downgrade", "cancel", "renew"]
    product_id: str
    product_name: str
    recurring: bool
    next_cycle_at: int
    current_product_name: str
    items: List[ProductItem]
    options: List[str]
    due_today: PriceCurrencyPair
    due_next_cycle: PriceCurrencyPair
