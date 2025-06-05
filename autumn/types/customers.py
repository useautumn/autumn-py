from typing import Optional

from pydantic import BaseModel

__all__ = ("Customer",)


class Customer(BaseModel):
    name: str
    email: str
    fingerprint: Optional[str] = None
