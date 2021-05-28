import collections

from eva import db

Environment = collections.namedtuple('Environment', ['db_engine', 'db_path'])

DEVELOPMENT = Environment('sqlite', 'db.sqlite')
TESTING = Environment('sqlite', 'test_db.sqlite')


def setup(environment=DEVELOPMENT):
    db.db.bind(environment.db_engine, environment.db_path, create_db=True)
    db.db.generate_mapping(create_tables=True)
