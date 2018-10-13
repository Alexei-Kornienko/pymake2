import os

from pymake2 import pymake


def import_makefile(path):
    if not os.path.exists(path):
        raise ValueError('Makefile %s doesn`t exist' % path)
    from importlib.machinery import SourceFileLoader

    makefileM = SourceFileLoader('makefileM', path).load_module()
    return makefileM


def parse(makefile_path):
    mfile = pymake.Makefile(makefile_path)
    module = import_makefile(makefile_path)
    for item in dir(module):
        if item.startswith('__'):
            continue  # Module private stuff
        obj = getattr(module, item)
        if isinstance(obj, pymake.Dependency):
            mfile.add_dep(item, obj)
        if isinstance(obj, pymake.Target):
            mfile.add_target(item, obj)
    return mfile
