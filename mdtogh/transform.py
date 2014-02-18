import os

def transform(path = None, gfm = False, username = None, password = None, toc = True, offline = False):
    if path == None:
        path = '.'
    if not os.path.exists(path):
        raise ValueError('File not found: ' + path)
    elif os.path.isdir(path):
        pass
    elif os.path.isfile(path):
        pass

    pass
