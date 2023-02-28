#!/usr/bin/env python

from io import open
from setuptools import setup

"""
:authors: Daniel "wendo" Wendland
:license: Apache License, Version 2.0, see LICENSE file
:copyright: (c) 2023 wendland0d
"""

version = '0.2.0'

with open('README.md', encoding='utf-8') as f:
    long_description = f.read()


setup(
    name='csgotm_py',
    version=version,

    author='wendland0d',
    author_email='wendland0d@gmail.com',

    description=(
        u'Python module for working with Market CS:GO API'
    ),
    long_description=long_description,
    long_description_context_type='text/markdown',

    url='https://github.com/wendland0d/csgotm-py',


    license='Apache License, Version 2.0, see LICENSE file',

    packages=['csgotm'],
    install_requires=['requests'],

    classifiers=[
        'License :: OSI Approved :: Apache Software License',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Developers',
        'Programming Language :: Python'
    ]


)