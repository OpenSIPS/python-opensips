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

""" MI Datagram implementation """

import socket
import os
from tempfile import NamedTemporaryFile
from .connection import Connection
from . import jsonrpc_helper

class Datagram(Connection):
    """ MI Datagram connection """

    def __init__(self, **kwargs):
        if "datagram_unix_socket" in kwargs:
            self.address = kwargs["datagram_unix_socket"]
            self.family = socket.AF_UNIX
            with NamedTemporaryFile(prefix="opensips_mi_reply_", dir="/tmp") as nt:
                self.recv_sock = nt.name
        elif "datagram_ip" in kwargs and "datagram_port" in kwargs:
            self.address = (kwargs["datagram_ip"], int(kwargs["datagram_port"]))
            self.family = socket.AF_INET
            self.recv_sock = None
        else:
            raise ValueError("Either datagram_unix_socket or both datagram_ip and datagram_port are required for Datagram")

        self.timeout = float(kwargs.get("datagram_timeout") or 0.1)
        self.recv_size = int(kwargs.get("datagram_buffer_size") or 32768)

    def execute(self, method: str, params: dict):
        jsoncmd = jsonrpc_helper.get_command(method, params)

        udp_socket = socket.socket(self.family, socket.SOCK_DGRAM)
        try:
            if self.recv_sock:
                udp_socket.bind(self.recv_sock)
            udp_socket.sendto(jsoncmd.encode(), self.address)
            udp_socket.settimeout(self.timeout)
            reply = udp_socket.recv(self.recv_size)
        except Exception as e:
            raise jsonrpc_helper.JSONRPCException(e)
        finally:
            if self.recv_sock:
                os.unlink(self.recv_sock)
            udp_socket.close()

        return jsonrpc_helper.get_reply(reply)

    def valid(self):
        return (True, None)

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
