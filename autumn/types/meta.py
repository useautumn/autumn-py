from __future__ import annotations

from enum import StrEnum
from typing import TYPE_CHECKING, Optional

from pydantic import BaseModel

if TYPE_CHECKING:
    from typing import Dict, Any

    Metadata = Dict[str, Any]


class AppEnv(StrEnum):
    PRODUCTION = "production"
    SANDBOX = "sandbox"


class AttachOption(BaseModel):
    feature_id: str
    quantity: int


class CustomerData(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    fingerprint: Optional[str] = None
