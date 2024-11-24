from conf import get_global_config as config


def read_out(type: str):
    items = []
    with open(f"{config().OUT_DIR}/lex/{type}.txt", "r", encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            items.append(line)
    return items

def read_res(type: str):
    items = []
    with open(f"{config().RES_DIR}/{type}.txt", "r", encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            items.append(line)
    return items

__all__ = [
    "read_out",
    "read_res"
]