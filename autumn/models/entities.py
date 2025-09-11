from typing import Dict, List, Literal, Optional

from pydantic import BaseModel

from .customers import CustomerFeature, CustomerInvoice, CustomerProduct
from .products import Product


class Entity(BaseModel):
    id: str
    name: str
    customer_id: str
    created_at: int
    env: str
    products: List[CustomerProduct]
    features: Dict[str, CustomerFeature]
    invoices: Optional[List[CustomerInvoice]] = None

