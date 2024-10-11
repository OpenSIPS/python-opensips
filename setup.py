#!/usr/bin/env python
##
## This file is part of the OpenSIPS Python Package
## (see https://github.com/OpenSIPS/python-opensips).
##
## This program is free software: you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation, either version 3 of the License, or
## (at your option) any later version.
##
## This program is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.
##
## You should have received a copy of the GNU General Public License
## along with this program. If not, see <http://www.gnu.org/licenses/>.
##

from setuptools import setup, find_packages

from opensips import version

setup(
    name="opensips",
    version=version.__version__,
    packages=find_packages(),
    install_requires=[],
    author="Darius Stefan",
    author_email="darius.stefan@opensips.org",
    description="OpenSIPS Python Packages",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url="https://github.com/OpenSIPS/python-opensips",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    scripts=['scripts/opensips-mi'],
    python_requires=">=3.6"
)
