import os.path
import re


def write(content: str, path: str) -> None:
    if not os.path.exists(path):
        dir = os.path.split(path)
        os.makedirs(dir[0], exist_ok=True)

    with open(path, 'a') as f:
        f.write(f'{content}\n')

def flush(path: str) -> None:
    if os.path.exists(path):
        with open(path, 'w') as f:
            f.write('')