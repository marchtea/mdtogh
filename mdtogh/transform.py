import os
from .renderer import render_file

def transform(path = None, gfm = False, username = None, password = None, toc = True, offline = False):
    if path == None:
        path = '.'
    if not os.path.exists(path):
        raise ValueError('File not found: ' + path)
    elif os.path.isdir(path):
        pass
    elif os.path.isfile(path):
        try:
            content, toc = render_file(path, gfm, username, password, toc, offline)
            f = open('tmp.html', 'w')
            f.write(content)
            f.close()
            print "done."
        except RuntimeError as ex:
            print "Error: ", ex
    else:
        raise ValueError('Not supported file: ' + path)
