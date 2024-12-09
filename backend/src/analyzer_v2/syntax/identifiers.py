from pydantic import BaseModel

class Identifier(BaseModel):
    type: str
    value: float|int|bool|None = None
    name: str
    count: int = 0


founded: list[Identifier] = []

def add_id(id:Identifier):
    global founded
    id.count = id.count+1
    for i in founded:
        if id.name == i.name:
            i.count += 1
            return i.count
    founded.append(id)
    return 1

def flush():
    global founded
    founded = []