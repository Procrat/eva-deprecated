from setuptools import setup
from codecs import open
from os import path


try:
    here = path.abspath(path.dirname(__file__))
    with open(path.join(here, 'README.md'), encoding='utf-8') as file_:
        long_description = file_.read()
except FileNotFoundError:
    # Only occurs when testing
    long_description = ''


setup(
    name='eva',
    version='0.1',
    description='Eva Virtual Assistant: your own life organiser',
    long_description=long_description,
    url='https://github.com/Procrat/eva',
    author='Stijn Seghers',
    author_email='stijnseghers@gmail.com',
    license='MIT',
    classifiers=[
        'Development Status :: 1 - Planning',
        'Environment :: Console',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: POSIX :: Linux',
        'Operating System :: MacOS',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Office/Business :: Scheduling',
        'Topic :: Other/Nonlisted Topic',
        'Topic :: Utilities'
    ],
    keywords='eva assistant organise life organiser',
    packages=['eva'],
    tests_require=['pytest'],
)
