from collections import defaultdict
import re


class regexdict(defaultdict):

    def __getitem__(self, key):
        for regex in self.keys():
            if re.search(regex, key, re.IGNORECASE) != None:
                return super().__getitem__(regex)
        return self.__missing__(key)

    def __missing__(self, key):
        if self.default_factory is None:
            raise KeyError()

        return self.default_factory(key)
