import os.path

def get_import_path(filename=''):
    import Products.GroupServer.imports

    path = os.path.dirname(Products.GroupServer.imports.__file__)
    if filename:
        path = os.path.join(path, filename)

    return path

def get_groupserver_path(filename=''):
    import Products.GroupServer

    path = os.path.dirname(Products.GroupServer.__file__)
    if filename:
        path = os.path.join(path, filename)

    return path


