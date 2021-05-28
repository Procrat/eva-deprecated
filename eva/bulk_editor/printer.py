def stringify(sections):
    return '\n'.join(stringify_section(section) for section in sections)


def stringify_section(section):
    return str(section)


if __name__ == "__main__":
    from eva import settings, db
    from eva.bulk_editor import parse
    from pathlib import Path

    settings.setup(settings.TESTING)

    path = (Path(__file__) / '..' / '..' / '..' / 'tests' / 'bulk_editor' /
            'todo_files' / 'todo_file').resolve()
    with open(str(path)) as file_:
        text = file_.read()
    sasdf = parse(text)
    import ipdb
    ipdb.set_trace()
    print(stringify(sasdf))
