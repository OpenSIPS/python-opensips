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

""" Helper to extract JSON from response """

import json
from collections import OrderedDict


class JsonBufferMaxAttempts(Exception):
    """ Raised when the max attempts is reached """


class JsonBuffer:

    """ Class that parses and handles partial Json Data """
    def __init__(self, max_retries=10):
        self.queue = []
        self.retries = 0
        self.max_retries = max_retries
        self.buf = ""

    def push(self, data):
        """ Pushes data into JsonBuffer """
        self.buf += data.decode("utf-8")

        # try to parse the json
        self.parse()
        if not self.queue:
            self.retries += 1

        if self.retries > self.max_retries:
            raise JsonBufferMaxAttempts()

    def pop(self):
        """ Retrieves a json from the buffer """
        if len(self.queue) == 0:
            return None
        self.retries = 0
        return self.queue.pop(0)

    def parse(self):
        """ Parses the current json buffer """
        while len(self.buf) > 0:
            try:
                json_decoder = json.JSONDecoder(object_pairs_hook=OrderedDict)
                json_obj, idx = json_decoder.raw_decode(self.buf)
                self.queue.append(json_obj)
                self.buf = self.buf[idx:]
            except json.JSONDecodeError:
                break

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
