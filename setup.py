#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import setuptools
import os
from pathlib import Path

here = Path(__file__).parent.resolve()
# See also: https://packaging.python.org/guides/single-sourcing-package-version/
version = {}
exec(here.joinpath("src", "ambiance", "__version__.py").read_text(), version)

# See also: https://github.com/kennethreitz/setup.py/blob/master/setup.py

NAME = 'ambiance'
VERSION = version["__version__"]
AUTHOR = 'Aaron Dettmann'
EMAIL = 'dettmann@kth.se'
DESCRIPTION = 'A full implementation of the ICAO standard atmosphere 1993'
URL = 'https://github.com/airinnova/ambiance/'
REQUIRES_PYTHON = '>=3.6.0'
REQUIRED = [
    'numpy',
    'scipy',
]
README = 'README.rst'
PACKAGE_DIR = 'src'
LICENSE = 'Apache License 2.0'

setuptools.setup(
    name=NAME,
    version=VERSION,
    author=AUTHOR,
    author_email=EMAIL,
    description=DESCRIPTION,
    long_description=here.joinpath(README).read_text(),
    url=URL,
    include_package_data=True,
    package_dir={'': PACKAGE_DIR},
    license=LICENSE,
    packages=[NAME],
    python_requires=REQUIRES_PYTHON,
    install_requires=REQUIRED,
    # See: https://pypi.org/classifiers/
    classifiers=[
        "Programming Language :: Python :: 3",
        'Programming Language :: Python :: 3.6',
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering",
        "Topic :: Scientific/Engineering :: Physics",
        "Topic :: Scientific/Engineering :: Atmospheric Science",
    ],
    project_urls={
        'Documentation': 'https://ambiance.readthedocs.io/',
        'Source': URL,
        'Tracker': URL + 'issues',
    },
)
