from pydantic import BaseModel


class PreExpertiseSelfCheckSchema(BaseModel):
    name: str = "pre_expertise_self_check"
