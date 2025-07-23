from typing import Optional, List

from pydantic import BaseModel

from .meta import AppEnv
from .products import ProductItem, FreeTrial
from .customers import PricingTableProduct

__all__ = ("AttachResponse", "CheckResponse")


class AttachResponse(BaseModel):
    customer_id: str
    code: str = "No code returned."
    message: str
    checkout_url: Optional[str] = None
    product_ids: List[str]
    success: Optional[bool] = None


class CheckResponse(BaseModel):
    allowed: bool
    customer_id: str
    code: str
    balance: Optional[float] = None
    feature_id: Optional[str] = None
    product_id: Optional[str] = None
    status: Optional[str] = None
    # TODO: add preview attribute


class TrackResponse(BaseModel):
    id: str
    code: str
    customer_id: str
    feature_id: Optional[str] = None
    event_name: Optional[str] = None


class UsageResponse(BaseModel):
    code: str
    customer_id: str
    feature_id: str


class BillingPortalResponse(BaseModel):
    url: str
    customer_id: str


class CreateProductResponse(BaseModel):
    autumn_id: str
    created_at: int
    id: str
    name: str
    env: AppEnv
    is_add_on: bool
    is_default: bool
    items: List[ProductItem]
    free_trial: Optional[FreeTrial] = None


GetProductResponse = CreateProductResponse


class ReferralCodeResponse(BaseModel):
    code: str
    customer_id: str
    created_at: int


class ReferralRedeemResponse(BaseModel):
    id: str
    customer_id: str
    reward_id: str


class ProductCancelResponse(BaseModel):
    success: bool
    message: str
    customer_id: str
    product_id: str


class PricingTableResponse(BaseModel):
    list: List[PricingTableProduct]
