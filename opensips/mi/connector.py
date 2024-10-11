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

from .fifo import FIFO
from .datagram import Datagram
from .http import HTTP
from .jsonrpc_helper import JSONRPCError, JSONRPCException

class OpenSIPSMIException(Exception):
    pass

class OpenSIPSMI():
    def __init__(self, conn="fifo", **kwargs):
        if conn == "fifo":
            if "fifo_file" not in kwargs:
                kwargs["fifo_file"] = "/var/run/opensips/opensips_fifo"
            if "fifo_file_fallback" not in kwargs:
                kwargs["fifo_file_fallback"] = "/tmp/opensips_fifo"
            if "fifo_reply_dir" not in kwargs:
                kwargs["fifo_reply_dir"] = "/tmp"
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
            raise OpenSIPSMIException("Error executing command: {}".format(e))
        except JSONRPCException as e:
            raise OpenSIPSMIException("Error with connection: {}. Is OpenSIPS running?".format(e))
        return ret_val
    
    def valid(self):
        if self.validated is not None:
            return self.validated
        self.validated = self.conn.valid()
        return self.validated
