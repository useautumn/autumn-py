from typing import Optional, List

from pydantic import BaseModel

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
    feature_id: str
    code: str
    balance: Optional[float] = None
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
