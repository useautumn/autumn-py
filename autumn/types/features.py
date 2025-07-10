from typing import Literal, List, Dict, Optional

from pydantic import BaseModel

from ..types.customers import CustomerProduct, CustomerFeature, CustomerInvoice

__all__ = ("Feature", "FeaturePreview", "Entity")


class Feature(BaseModel):
    feature_id: str
    quantity: int


class FeaturePreview(BaseModel):
    title: str
    message: str
    scenario: Literal["usage_limit", "feature_flag"]
    feature_id: str
    feature_name: str
    upgrade_product_id: str


class Entity(BaseModel):
    id: str
    name: str
    customer_id: str
    created_at: int
    env: str
    products: List[CustomerProduct]
    features: Dict[str, CustomerFeature]
    invoices: Optional[List[CustomerInvoice]] = None
