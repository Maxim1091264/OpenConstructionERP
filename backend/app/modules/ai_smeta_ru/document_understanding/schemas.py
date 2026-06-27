from pydantic import BaseModel


class DocumentUnderstandingSchema(BaseModel):
    name: str = "document_understanding"
