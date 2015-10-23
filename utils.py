from collections import defaultdict
import re


class regexdict(defaultdict):
    """Maps regexes to some values."""

    def __getitem__(self, key):
        for regex in self.keys():
            if re.match(regex, key, re.IGNORECASE) is not None:
                return super().__getitem__(regex)
        return self.__missing__(key)

    def __missing__(self, key):
        if self.default_factory is None:
            raise KeyError()

        return self.default_factory(key)
