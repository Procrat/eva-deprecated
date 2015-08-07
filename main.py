#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import ui
import actions
import exceptions
import settings


def setup():
    settings.setup()


def main():
    try:
        while True:
            action = ui.let_choose('What do you want to do?',
                                   actions.MAIN_ACTIONS)
            if action is not None:
                action.run()
    except (exceptions.QuitException, KeyboardInterrupt):
        pass


if __name__ == "__main__":
    setup()
    main()
