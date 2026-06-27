from pydantic import BaseModel


class EstimatorPackageSchema(BaseModel):
    name: str = "estimator_package"
