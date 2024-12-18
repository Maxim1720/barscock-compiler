import os.path


def exists(content, path):
    if os.path.exists(path):
        with open(path, 'r') as f:
            for line in f.readlines():
                # print(f'line:{line.strip()}')
                if line.strip() == content:
                    return True

    return False



def is_tw(token):
    with open(f'{os.getcwd()}/res/tw.txt', 'r') as f:
        for line in f.readlines():
            if line.strip() == token:
                return True
    return False


def is_tl(token):
    with open(f'{os.getcwd()}/res/tl.txt', 'r') as f:
        for line in f.readlines():
            if line.strip() == token:
                return True
    return False