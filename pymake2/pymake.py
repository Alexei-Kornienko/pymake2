import os


class Dependency:
    def __init__(self, name):
        self._name = name

    def get_timestamp(self):
        return os.path.getmtime(self._name)
