from pydantic import BaseModel


class FoundedIdentifier(BaseModel):
    name: str
    defined: int = 0
    type: str|None
    excluded: bool| None = None