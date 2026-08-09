import os

def isfile(path: str) -> bool:
    return (True if os.stat(path)[0] & 32768 else False)


def isdir(path: str) -> bool:
    return (True if os.stat(path)[0] & 16384 else False)


def exists(path: str) -> bool:
    try:
        os.stat(path)
        return True
        
    except OSError:
        return False
        
    


def mkdirs(path: str):
    part = ""
    for folder in path.split("/"):
        part += folder + "/"
        if not exists(part):
            os.mkdir(part)


def remove(path: str):
    if exists(path):
        if isdir(path):
            for subpath in os.listdir(path):
                remove(path + "/" + subpath)
            os.rmdir(path)
        else:
            os.remove(path)

