from pydantic import BaseModel


class AiSmetaRuStatus(BaseModel):
    module: str
    status: str
