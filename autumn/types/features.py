from typing import Literal

from pydantic import BaseModel


class Feature(BaseModel):
    feature_id: str
    quantity: int


class FeaturePreview(BaseModel):
    title: str
    message: str
    scenario: Literal["usage_limit", "feature_flag"]
    feature_id: str
    feature_name: str
    upgrade_product_id: str


__all__ = ("Feature", "FeaturePreview")
