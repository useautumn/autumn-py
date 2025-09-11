from typing import Dict, List, Optional

from pydantic import BaseModel

from .customers import CustomerFeature, CustomerInvoice, CustomerProduct
from .env import AppEnv


class Entity(BaseModel):
    id: str
    name: str
    customer_id: str
    created_at: int
    env: AppEnv
    products: List[CustomerProduct]
    features: Dict[str, CustomerFeature]
    invoices: Optional[List[CustomerInvoice]] = None
