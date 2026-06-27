from pydantic import BaseModel


class AssumptionEngineSchema(BaseModel):
    name: str = "assumption_engine"
