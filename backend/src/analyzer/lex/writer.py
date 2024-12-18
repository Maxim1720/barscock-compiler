import os.path
import re


def write(content: str, path: str) -> None:
    if not os.path.exists(path):
        dir = "/".join(re.split('/', path)[:-1])
        os.makedirs(dir, exist_ok=True)

    with open(path, 'a') as f:
        f.write(f'{content}\n')

def flush(path: str) -> None:
    if os.path.exists(path):
        with open(path, 'w') as f:
            f.write('')