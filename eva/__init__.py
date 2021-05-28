# Monkey patches \o/
import parsley

parsley.ParseError.__hash__ = lambda self: self.position
