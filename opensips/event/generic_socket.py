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

""" Defines a generic socket """

from abc import ABC, abstractmethod

class GenericSocket(ABC):

    """ Abstract class for a socket generic implementation """

    @abstractmethod
    def __init__(self, **kwargs):
        pass

    @abstractmethod
    def create(self) -> str:
        """ Creates a socket """

    @abstractmethod
    def read(self):
        """ Reads data on the socket """

    @abstractmethod
    def destroy(self):
        """ Destroys the socket """
