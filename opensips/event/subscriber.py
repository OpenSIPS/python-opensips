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

from ..mi import MI, OpenSIPSMIException
from .datagram import Datagram
from .stream import Stream
from threading import Thread, Event

class OpenSIPSEventException(Exception):
    pass

class OpenSIPSEvent():
    def __init__(self, mi: MI, type: str, **kwargs):
        self.mi = mi
        self.kwargs = kwargs

        if type == "datagram":
            self.socket = Datagram(**kwargs)
        elif type == "stream":
            self.socket = Stream(**kwargs)
        else:
            raise ValueError("Invalid event type")

    def subscribe(self, event: str, callback, expire=None):
        try:
            if expire is None:
                ret_val = self.mi.execute("event_subscribe", [event, self.socket.sock_name])
            else:
                ret_val = self.mi.execute("event_subscribe", [event, self.socket.sock_name, expire])

            if ret_val != "OK":
                raise OpenSIPSEventException("Failed to subscribe to event")
            
            self.socket.create()
            self.thread_stop = Event()
            self.thread_stop.clear()
            self.thread = Thread(target=self.socket.handle, args=(callback, self.thread_stop))
            self.thread.start()

        except OpenSIPSMIException as e:
            raise e
        except Exception as e:
            raise OpenSIPSEventException("Failed to subscribe to event: {}".format(e))
        
    def unsubscribe(self, event: str):
        try:
            ret_val = self.mi.execute("event_subscribe", [event, self.socket.sock_name, 0])

            if ret_val != "OK":
                raise OpenSIPSEventException("Failed to unsubscribe from event")
            
        except OpenSIPSMIException as e:
            raise e
        
    def stop(self):
        self.thread_stop.set()
        self.thread.join()
