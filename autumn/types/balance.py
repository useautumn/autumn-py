from typing import Optional

from pydantic import BaseModel


class Balance(BaseModel):
    feature_id: str
    balance: int
    required_balance: Optional[int] = None
