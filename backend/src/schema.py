from pydantic import BaseModel

from backend.src.analyzer.lexical.const import State


class CodeRequestSchema(BaseModel):
    data: str

class AnalyzeResponseSchema(BaseModel):
    tw: list[str]
    tl: list[str]
    tn: list[str]
    ti: list[str]
    state: str
