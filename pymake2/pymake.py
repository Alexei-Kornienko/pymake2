import os
import inspect

from pymake2 import utility as util


class Makefile:
    def __init__(self, path):
        self._path = path
        self.targets = {}
        self.deps = {}
        self.debug = False
        self.highlight_errors = False
        self.highlight_warnings = False

    def add_target(self, name, target):
        self.targets[name] = target
        target.bind_makefile(self)

    def add_dep(self, name, dep):
        self.deps[name] = dep


class Dependency:
    def __init__(self, name):
        self._name = name

    def get_timestamp(self):
        return os.path.getmtime(self._name)

    def __str__(self):
        return self._name

    def build(self):
        pass


class Target(Dependency):
    def __init__(self, func, name=None):
        if not name:
            name = func.__name__
        super(Target, self).__init__(name)
        self._builder = func
        self._deps = inspect.getargspec(func).args
        self._makefile = None

    def get_timestamp(self):
        try:
            return super(Target, self).get_timestamp()
        except FileNotFoundError:
            return None

    def bind_makefile(self, mfile):
        self._makefile = mfile

    def get_deps(self):
        return [self._makefile.deps[dep] for dep in self._deps]

    def is_up_to_date(self):
        stamp = self.get_timestamp()
        if not stamp:
            return False
        try:
            deps_stamps = [dep.get_timestamp() for dep in self.get_deps()]
        except FileNotFoundError as e:
            raise ValueError('Missing required dependency - %s' % e)
        if deps_stamps:
            return stamp > max(deps_stamps)
        return True

    def build(self):
        if self.is_up_to_date():
            util.print_color('Target "%s" is up to date' % self._name, util.tty_colors_cmds.On_Green)
            return
        deps = self.get_deps()
        for dep in deps:
            dep.build()
        util.print_color('Building Target "%s"' % self._name, util.tty_colors_cmds.On_Cyan)
        self._builder(*deps)
