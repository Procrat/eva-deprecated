class QuitException(Exception):
    pass


class MultipleChoicesWithSameMnemonicException(Exception):
    pass


class MissingDependencyException(Exception):
    def __init__(self, dependency):
        self.message = 'You seem to be missing a dependency: "%s"' % dependency
