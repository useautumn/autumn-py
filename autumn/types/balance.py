from pydantic import BaseModel


class Balance(BaseModel):
    feature_id: str
    required_balance: int
    balance: int
