from pydantic import BaseModel


class AiSmetaCommonSchema(BaseModel):
    name: str = "common"
