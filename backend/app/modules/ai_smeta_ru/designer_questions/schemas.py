from pydantic import BaseModel


class DesignerQuestionsSchema(BaseModel):
    name: str = "designer_questions"
