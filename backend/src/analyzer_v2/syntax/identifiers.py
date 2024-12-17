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

def get_id_by_name(name):
    return list(filter(lambda x: x.name == name, founded))[0]

def id_exists(name):
    return len(list(filter(lambda x: x.name == name, founded))) > 0