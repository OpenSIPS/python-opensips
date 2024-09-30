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

import socket
from .generic import GenericSocket

class Datagram(GenericSocket):
    def __init__(self, **kwargs):
        self.ip = None
        self.port = None

        if "unix_path" in kwargs:
            self.sock_name = kwargs["unix_path"]
        elif "ip" in kwargs and "port" in kwargs:
            self.ip = kwargs["ip"]
            self.port = kwargs["port"]
            self.sock_name = f"udp:{self.ip}:{self.port}"
        else:
            raise ValueError("ip and port or unix_path is required for Datagram connector")
    
    def create(self):
        if self.ip is not None:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.sock.bind((self.ip, self.port))
        else:
            self.sock = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)
            self.sock.bind(self.sock_name)

    def handle(self, callback, stop):
        while not stop:
            data = self.sock.recv(1024)
            callback(data)

