#!/usr/bin/env python
#
# This file is part of the OpenSIPS Python Package
# (see https://github.com/OpenSIPS/python-opensips).
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#


""" Abstract implementation of an MI connection """

from abc import ABC, abstractmethod


class Connection(ABC):

    """ Abstract MI Connection """

    @abstractmethod
    def __init__(self, **kwargs):
        pass

    @abstractmethod
    def execute(self, method: str, params: dict):
        """ Executes an MI Command """

    @abstractmethod
    def valid(self):
        """ Checks if an MI connection is valid """

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
