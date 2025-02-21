from pydantic import BaseModel


class InputQuestionSchema(BaseModel):
    question: str


class OutputQuestionSchema(BaseModel):
    answer: str | None = None