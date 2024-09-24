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

from ..mi import MI
from .socket import Datagram, Stream

class Event():
    def __init__(self, mi: MI, type: str, **kwargs):
        self.mi = mi
        self.kwargs = kwargs

        if type == "datagram":
            self.type = Datagram(**kwargs)
        elif type == "stream":
            self.type = Stream(**kwargs)
        else:
            raise ValueError("Invalid event type")

        self.type.create()
        self.cb = None

    def subscribe(self, event: str, callback, expire=3600):
        # callback should be a function that takes a socket as an argument
        print(self.mi.execute("event_subscribe", [event, self.type.sock_name, expire]))
        self.cb = callback

    def get_socket(self):
        return self.type.sock

    def callback(self):
        return self.cb(self.type.sock)
