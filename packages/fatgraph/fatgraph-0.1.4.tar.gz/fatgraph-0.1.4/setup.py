#!/usr/bin/env python
# coding=utf-8

from distutils.core import setup

# noinspection PyArgumentList
setup(
    name='fatgraph',
    version='0.1.4',
    author='Yuki Koyanagi',
    author_email='yukiswt@gmail.com',
    packages=['fatgraph'],
    #url='https://github.com/eseraygun/python-alignment',
    license='BSD 3-Clause License',
    requires=['permutation','numpy',],
    package_dir={'fatgraph': 'fatgraph'},
    scripts=['scripts/compute.py',]
)
