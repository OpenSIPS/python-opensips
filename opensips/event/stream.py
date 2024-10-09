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
from .generic_socket import GenericSocket

class Stream(GenericSocket):
    def __init__(self, **kwargs):
        if "ip" not in kwargs:
            raise ValueError("ip is required for Stream connector")
        if "port" not in kwargs:
            raise ValueError("port is required for Stream connector")
        
        self.ip = kwargs["ip"]
        self.port = int(kwargs["port"])
        self.sock_name = f"tcp:{self.ip}:{self.port}"

    def create(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((self.ip, self.port))
        self.sock.setblocking(False)
        self.sock.listen(1)

    def handle(self, callback, stop):
        while not stop.is_set():
            try:
                conn, _ = self.sock.accept()
                conn.setblocking(True)
                with conn:
                    data = conn.recv(1024)
                    if not data:
                        continue
                    callback(data)
            except BlockingIOError:
                pass
    
    def destroy(self):
        self.sock.close()
        self.sock = None
