from typing import Dict, List, Literal, Optional

from pydantic import BaseModel

from .env import AppEnv
from .customers import CustomerFeature, CustomerInvoice, CustomerProduct
from .products import Product


class Entity(BaseModel):
    id: str
    name: str
    customer_id: str
    created_at: int
    env: AppEnv
    products: List[CustomerProduct]
    features: Dict[str, CustomerFeature]
    invoices: Optional[List[CustomerInvoice]] = None

