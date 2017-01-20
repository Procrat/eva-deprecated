# Eva - Eva Virtual Assistant    [![Build status](https://travis-ci.org/Procrat/eva.png?branch=master)](https://travis-ci.org/Procrat/eva)

Your own free personal assistant


## About

Eva aims to be an application with a personality to manage your life when you
don't feel like doing that yourself.
It currently does this by managing your todo-list, but hopefully it will soon
enough become an agenda / scheduler / focus booster / reminder, all in one.

It borrows from various productivity and motivation concepts like GTD,
Pomodoro, the Eisenhower scheme, flow, focussing on one task, small-chunking
work, eating the frog, etc.


## WORK IN PROGRESS

This project hasn't reached an alpha state yet. As a matter of fact, it is being
completely rewritten in a more sensible approach, trying to reach an MVP sooner
so we can reap the benefits of dogfooding!


## Installation

Soon `setup.py` will cover dependencies, but for now please install
dependencies manually.
`pip install -r requirements.txt`

### Linux

Make sure `libnotify` and `at` are installed. Also make sure the `at` daemon is
running (and started on boot).

### Mac OS

Run `pip install -r requirements_osx.txt`


## Usage

At the moment you can just run `main.py` using Python 3.


## Acknowledgements

Many thanks go out to [Personal Productivity
@StackExchange](http://productivity.stackexchange.com), [zen
habits](http://zenhabits.net) and [GTD](http://gettingthingsdone.com) for
inspiring me!
