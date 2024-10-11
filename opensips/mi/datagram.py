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

""" MI Datagram implementation """

import socket
from .connection import Connection
from . import jsonrpc_helper

class Datagram(Connection):

    """ MI Datagram connection """

    def __init__(self, **kwargs):
        if "datagram_ip" not in kwargs:
            raise ValueError("datagram_ip is required for Datagram connector")

        if "datagram_port" not in kwargs:
            raise ValueError("datagram_port is required for Datagram connector")

        self.ip = kwargs["datagram_ip"]
        self.port = int(kwargs["datagram_port"])

    def execute(self, method: str, params: dict):
        jsoncmd = jsonrpc_helper.get_command(method, params)

        udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            udp_socket.sendto(jsoncmd.encode(), (self.ip, self.port))
            udp_socket.settimeout(5.0)
            reply = udp_socket.recv(32768)
        except Exception as e:
            raise jsonrpc_helper.JSONRPCException(e)
        finally:
            udp_socket.close()
        return jsonrpc_helper.get_reply(reply)

    def valid(self):
        return (True, None)
