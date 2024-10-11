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

""" Implements Datagram Connection """

import socket
from .generic_socket import GenericSocket

class Datagram(GenericSocket):

    """ Datagram implementation of a socket """

    def __init__(self, **kwargs):
        self.ip = None
        self.port = None
        self.sock = None

        if "unix_path" in kwargs:
            self.sock_name = kwargs["unix_path"]
        elif "ip" in kwargs and "port" in kwargs:
            self.ip = kwargs["ip"]
            self.port = int(kwargs["port"])
        else:
            raise ValueError("ip and port or unix_path is required for Datagram connector")

    def create(self):
        if self.ip is not None:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.sock.bind((self.ip, self.port))
            self.ip, self.port = self.sock.getsockname()
            if self.ip == "0.0.0.0":
                hostname = socket.gethostname()
                self.ip = socket.gethostbyname(hostname)
            self.sock_name = f"udp:{self.ip}:{self.port}"
        else:
            self.sock = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)
            self.sock.bind(self.sock_name)
        # we are waiting blocking, so we don't have to change this
        self.sock.settimeout(0.1)
        return self.sock_name

    def read(self):
        try:
            return self.sock.recv(65535)
        except socket.timeout:
            return None

    def destroy(self):
        if not self.sock:
            return
        self.sock.close()
        self.sock = None
