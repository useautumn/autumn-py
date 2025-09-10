from typing import Optional, List

from pydantic import BaseModel

from .meta import AppEnv, CheckoutLine, AttachOption, Cycle, QueryDP
from .products import ProductItem, FreeTrial, Product
from .customers import PricingTableProduct, Customer
from .features import FeaturePreview
from .products import ProductPreview

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
    feature_preview: Optional[FeaturePreview] = None
    product_preview: Optional[ProductPreview] = None


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
    created_at: int
    id: str
    name: str
    env: AppEnv
    version: int
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


class CheckoutLine(BaseModel):
    description: str
    amount: float
    item: ProductItem


class CheckoutNextCycle(BaseModel):
    starts_at: int
    total: float


class CheckoutResponse(BaseModel):
    url: Optional[str] = None
    customer_id: str
    has_prorations: bool
    lines: List[CheckoutLine]
    total: float
    currency: str
    options: List[AttachOption]
    product: Optional[Product] = None
    current_product: Optional[Product] = None
    next_cycle: Optional[CheckoutNextCycle] = None


class ListProductResponse(BaseModel):
    list: List[Product]


class ListCustomerResponse(BaseModel):
    list: List[Customer]
    total: int
    limit: int
    offset: int


class QueryResponse(BaseModel):
    list: List[QueryDP]
