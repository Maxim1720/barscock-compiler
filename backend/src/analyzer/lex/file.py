import os.path


def exists(content, path):
    if os.path.exists(path):
        with open(path, 'r') as f:
            for line in f.readlines():
                # print(f'line:{line.strip()}')
                if line.strip() == content:
                    return True

    return False