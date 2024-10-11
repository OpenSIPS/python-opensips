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

""" MI FIFO implementation """

import os
import sys
import time
import errno

from .connection import Connection
from . import jsonrpc_helper

class FIFO(Connection):

    """ MI FIFO Connection """

    REPLY_FIFO_FILE_TEMPLATE = "opensips_fifo_reply_{}_{}"

    def __init__(self, **kwargs):
        if "fifo_file" not in kwargs:
            raise ValueError("fifo_file is required for FIFO connector")
        if "fifo_file_fallback" not in kwargs:
            raise ValueError("fifo_file_fallback is required for FIFO connector")
        if "fifo_reply_dir" not in kwargs:
            raise ValueError("fifo_reply_dir is required for FIFO connector")

        self.fifo_file = kwargs["fifo_file"]
        self.fifo_file_fallback = kwargs["fifo_file_fallback"]
        self.fifo_reply_dir = kwargs["fifo_reply_dir"]

    def execute(self, method: str, params: dict):
        # check if the environment is valid
        valid, msg = self.valid()
        if not valid:
            raise jsonrpc_helper.JSONRPCException(msg)
        jsoncmd = jsonrpc_helper.get_command(method, params)

        reply_fifo_file_name = self.REPLY_FIFO_FILE_TEMPLATE\
                        .format(os.getpid(), str(time.time()).replace(".", "_"))
        reply_fifo_file_path = os.path.join(self.fifo_reply_dir, reply_fifo_file_name)

        try:
            os.unlink(reply_fifo_file_path)
        except OSError as e:
            if os.path.exists(reply_fifo_file_path):
                raise jsonrpc_helper.JSONRPCException(
                    f"Could not remove old reply FIFO file {reply_fifo_file_path}: {e}")

        try:
            os.mkfifo(reply_fifo_file_path)
            os.chmod(reply_fifo_file_path, 0o666)
        except OSError as e:
            raise jsonrpc_helper.JSONRPCException(
                f"Could not create reply FIFO file {reply_fifo_file_path}: {e}")

        if not os.path.exists(self.fifo_file):
            raise jsonrpc_helper.JSONRPCException(
                "FIFO file {self.fifo_file} does not exist")

        fifocmd = f":{reply_fifo_file_name}:{jsoncmd}"
        try:
            with open(self.fifo_file, "w", encoding="utf-8") as fifo:
                fifo.write(fifocmd)
        except Exception as e:
            raise jsonrpc_helper.JSONRPCException(
                "Could not access FIFO file {self.fifo_file}: {e}")

        reply = None
        try:
            with open(reply_fifo_file_path, "r", encoding="utf-8") as reply_fifo:
                reply = reply_fifo.readline()
        except KeyboardInterrupt:
            sys.exit(-1)
        finally:
            os.unlink(reply_fifo_file_path)

        return jsonrpc_helper.get_reply(reply)

    def valid(self):
        opensips_fifo = self.fifo_file
        if not os.path.exists(opensips_fifo):
            opensips_fifo = self.fifo_file_fallback
            if not os.path.exists(opensips_fifo):
                msg1 = f"FIFO file {self.fifo_file} does not exist"
                msg2 = f"nor does fallback file {self.fifo_file_fallback}"
                return (False, [f"{msg1}, {msg2}", "Is OpenSIPS running?"])
        try:
            with open(opensips_fifo, "w", encoding="utf-8"):
                pass
        except OSError as e:
            extra = []
            if e.errno == errno.EACCES:
                sticky = self.get_sticky(os.path.dirname(opensips_fifo))
                if sticky:
                    extra = ["starting with Linux kernel 4.19, processes can " +
                            "no longer read from FIFO files ",
                            "that are saved in directories with sticky " +
                            f"bits (such as {sticky})",
                            "and are not owned by the same user the " +
                            "process runs with. ",
                            "To fix this, either store the file in a non-sticky " +
                            "bit directory (such as /var/run/opensips), ",
                            "or disable fifo file protection using " +
                            "'sysctl fs.protected_fifos=0' (NOT RECOMMENDED)"]
            msg = f"Could not access FIFO file {opensips_fifo}: {e}"
            return (False, [msg] + extra)
        self.fifo_file = opensips_fifo
        return (True, None)

    def get_sticky(self, path):
        """ returns whether a path has sitcky bit or not """
        if path == "/":
            return None
        if os.stat(path).st_mode & 0o1000 == 0o1000:
            return path
        return self.get_sticky(os.path.split(path)[0])
