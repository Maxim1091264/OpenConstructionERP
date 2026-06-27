from pydantic import BaseModel


class CompletenessCheckerSchema(BaseModel):
    name: str = "completeness_checker"
