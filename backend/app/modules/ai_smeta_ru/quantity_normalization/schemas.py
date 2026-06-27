from pydantic import BaseModel


class QuantityNormalizationSchema(BaseModel):
    name: str = "quantity_normalization"
