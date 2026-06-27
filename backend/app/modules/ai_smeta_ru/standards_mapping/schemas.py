from pydantic import BaseModel


class StandardsMappingSchema(BaseModel):
    name: str = "standards_mapping"
