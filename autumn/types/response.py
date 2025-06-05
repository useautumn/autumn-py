from typing import Optional, List, Literal

from pydantic import BaseModel

from .balance import Balance

__all__ = ("AttachResponse", "CheckResponse")


class AttachResponse(BaseModel):
    code: str
    message: str
    checkout_url: str
    customer_id: str
    product_ids: List[str]
    success: Optional[bool] = None


class CheckResponse(BaseModel):
    allowed: bool
    customer_id: str
    feature_id: str
    code: str
    balance: Balance


class TrackResponse(BaseModel):
    id: str
    code: str
    customer_id: str
    feature_id: str


class CreateCustomerResponse(BaseModel):
    id: str
    created_at: int
    name: str
    email: str
    fingerprint: Optional[str] = None
    stripe_id: Optional[str] = None
    env: Literal["production", "sandbox"]
