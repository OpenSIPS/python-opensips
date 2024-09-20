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

from .connector import HTTP, Datagram, FIFO
from .jsonrpc_helper import JSONRPCError, JSONRPCException

class MI():
    def __init__(self, conn: str, **kwargs):
        if conn == "fifo":
            self.conn = FIFO(**kwargs)
        elif conn == "datagram":
            self.conn = Datagram(**kwargs)
        elif conn == "http":
            self.conn = HTTP(**kwargs)
        else:
            raise ValueError("Invalid connector type")

        self.validated = None
    
    def execute(self, cmd, params=[]):
        try:
            ret_val = self.conn.execute(cmd, params)
        except JSONRPCError as e:
            raise Exception("Error executing command: {}".format(e))
        except JSONRPCException as e:
            raise Exception("Error with connection: {}. Is OpenSIPS running?".format(e))
        return ret_val
    
    def valid(self):
        if self.validated is not None:
            return self.validated
        self.validated = self.conn.valid()
        return self.validated
