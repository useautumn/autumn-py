from pydantic import BaseModel


class Customer(BaseModel):
    name: str
    email: str
    fingerprint: str
