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

""" Module that implements an OpenSIPS Event Handler to manage events subscriptions """

from ..mi import OpenSIPSMI, OpenSIPSMIException
from .event import OpenSIPSEvent, OpenSIPSEventException
from .datagram import Datagram
from .stream import Stream

class OpenSIPSEventHandler():

    """ Implementation of the OpenSIPS Event Handler"""

    def __init__(self, mi: OpenSIPSMI = None, _type: str = None, **kwargs):
        if mi:
            self.mi = mi
        else:
            self.mi = OpenSIPSMI()
        if _type:
            self._type = _type
        else:
            self._type = "datagram"
        self.kwargs = kwargs
        self.events = {str: OpenSIPSEvent}

    def __new_socket__(self):
        if self._type == "datagram":
            return Datagram(**self.kwargs)
        elif self._type == "stream":
            return Stream(**self.kwargs)
        else:
            raise ValueError("Invalid event type")

    def subscribe(self, event_name: str, callback, expire=None):
        return OpenSIPSEvent(self, event_name, callback, expire)

    def unsubscribe(self, event_name: str):
        self.events[event_name].unsubscribe()

    def __mi_subscribe__(self, event_name: str, sock_name: str, expire=None):
        try:
            if expire is None:
                ret_val = self.mi.execute("event_subscribe", [event_name, sock_name])
            else:
                ret_val = self.mi.execute("event_subscribe", [event_name, sock_name, expire])

            if ret_val != "OK":
                raise OpenSIPSEventException("Failed to subscribe to event")
        except OpenSIPSMIException as e:
            raise e

    def __mi_unsubscribe__(self, event_name: str, sock_name: str):
        try:
            ret_val = self.mi.execute("event_subscribe", [event_name, sock_name, 0])

            if ret_val != "OK":
                raise OpenSIPSEventException("Failed to unsubscribe from event")
        except OpenSIPSMIException as e:
            raise e