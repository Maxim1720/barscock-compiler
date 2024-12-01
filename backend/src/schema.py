from pydantic import BaseModel


class CodeRequestSchema(BaseModel):
    data: str

class AnalyzeResponseSchema(BaseModel):
    tw: list[str]
    tl: list[str]
    tn: list[str]
    ti: list[str]
    state: str
