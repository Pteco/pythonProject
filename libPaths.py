from os import walk
from os.path import join, dirname


class Paths:
    _curdir = dirname(__file__)

    def __init__(self):
        self.__paths = {}

    def home(self):
        return self._curdir

    def assets(self):
        for base, dirts, _ in walk(join(self._curdir, 'assets')):
            for dirt in dirts:
                self.__paths[dirt] = join(base, dirt)
        return self.__paths

    def data(self):
        for base, dirts, _ in walk(join(self._curdir, 'data')):
            for dirt in dirts:
                self.__paths[dirt] = join(base, dirt)
        return self.__paths

    def __getitem__(self, item):
        return self.__paths[item]

    @property
    def paths(self):
        return self.__paths

    def __str__(self) -> str:
        return f'{self.__class__.__name__}({self.paths})'
