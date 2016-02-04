def setup():
    import db
    db.db.bind('sqlite', 'test_db.sqlite', create_db=True)
    db.db.generate_mapping(create_tables=True)
