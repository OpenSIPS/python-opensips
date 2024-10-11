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

"""
This module contains helper functions to build and parse JSONRPC commands
"""

import json
from random import randint
from collections import OrderedDict

try:
    from json.decoder import JSONDecodeError
except ImportError: # JSONDecodeError is not available in  python3.4
    JSONDecodeError = ValueError

class JSONRPCException(Exception):
    """ JSONRPC generic exception """

class JSONRPCError(JSONRPCException):

    """ JSONRPC parsing exception """

    def __init__(self, code, message, data=None):
        self.code = code
        self.message = message
        self.data = data

    def get_data(self) -> str:
        """ Returns the data of the exception """
        return self.data

    def __str__(self) -> str:
        data = f" ({self.data})" if self.data else ""
        return f"{self.code}: {self.message}{data}"

def get_command(method, params=None) -> str:

    """ Builds a JSONRPC command and returns it """

    cmd = {
            'jsonrpc': '2.0',
            'id': str(randint(0, 32767)),
            'method': method,
            'params': params if params else {}
    }
    return json.dumps(cmd)

def get_reply(cmd) -> OrderedDict:

    """ Parses the reply and returns it as a OrderedDict """
    try:
        j = json.loads(cmd, object_pairs_hook=OrderedDict)
        if isinstance(j.get('error'), dict):
            raise JSONRPCError(j['error'].get('code', 500),
                               j['error'].get('message'),
                               j['error'].get('data'))
        if 'result' not in j:
            raise JSONRPCError(-32603, 'Internal error')
        return j['result']
    except JSONDecodeError as exc:
        raise JSONRPCException(f"could not decode json: '{cmd}'") from exc
