from typing import Literal, List

from pydantic import BaseModel


class PriceCurrencyPair(BaseModel):
    price: float
    currency: str


class ProductPreviewItem(BaseModel):
    price: PriceCurrencyPair
    description: str


class ProductPreview(BaseModel):
    title: str
    message: str
    scenario: Literal["upgrade", "downgrade", "cancel", "renew", "scheduled", "active"]
    product_id: str
    product_name: str
    recurring: bool
    next_cycle_at: bool
    current_product_name: str
    items: List[ProductPreviewItem]
    due_today: PriceCurrencyPair
    due_next_cycle: PriceCurrencyPair
