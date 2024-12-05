import os
import re

from src.files import read_res
from .types import FoundedIdentifier
from src.conf import get_global_config


def create_ti():
    identifiers = read_res("ti")
    dir_path = get_global_config().OUT_DIR + "/symantic"
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    path_to_file = f"{dir_path}/ti.txt"
    items = []
    for i in identifiers:
        item = {
            "val": i,
            "type": None,
            "defined": 0
        }
        items.append(item)
    with open(path_to_file, "w") as f:
        for item in items:
            f.write(f"{item['val']} {item['defined']} {item['type']}\n")


def get_identifiers_from_file() -> list[FoundedIdentifier]:
    with open(get_global_config().OUT_DIR + "/symantic/ti.txt") as f:
        items: list[FoundedIdentifier] = []
        for i in f.readlines():
            splitted = re.split(' ', i)
            items.append(
                FoundedIdentifier(**{
                    'name': splitted[0],
                    'type': splitted[2].strip(),
                    'defined': int(splitted[1]),
                })
            )
        return items