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

""" Module that implements OpenSIPS Event behavior """

import time
from threading import Thread, Event
from ..mi import OpenSIPSMIException
from .json_helper import JsonBuffer, JsonBufferMaxAttempts


class OpenSIPSEventException(Exception):
    """ Exceptions generated by OpenSIPS Events """


class OpenSIPSEvent():  # pylint: disable=too-many-instance-attributes

    """ Implementation of the OpenSIPS Event """

    def __init__(self, handler, name: str, callback, expire=None):
        self._handler = handler
        self.name = name
        self.callback = callback
        self.thread = None
        self.thread_stop = Event()
        self.thread_stop.clear()
        self.buf = JsonBuffer()
        if expire is not None:
            self.expire = expire
            self.reregister = False
        else:
            self.expire = 3600
            self.reregister = True

        try:
            self.socket = self._handler.__new_socket__()
            self._handler.__mi_subscribe__(self.name,
                                           self.socket.create(),
                                           self.expire)
            self.last_subscription = time.time()
            self._handler.events[self.name] = self
            self.thread = Thread(target=self.handle, args=(callback,))
            self.thread.start()
        except OpenSIPSEventException as e:
            raise e
        except OpenSIPSMIException as e:
            raise e
        except ValueError as e:
            raise OpenSIPSEventException("Invalid arguments") from e

    def handle(self, callback):
        """ Handles the event callbacks """
        while not self.thread_stop.is_set():
            if self.reregister and \
                    time.time() - self.last_subscription > self.expire - 60:
                try:
                    self.resubscribe()
                except Exception:  # pylint: disable=broad-exception-caught
                    callback(None)
                    break
            elif not self.reregister and \
                    time.time() - self.last_subscription > self.expire:
                callback(None)
                break

            data = self.socket.read()
            if not data:
                continue

            try:
                self.buf.push(data)
                j = self.buf.pop()
                while j:
                    callback(j)
                    j = self.buf.pop()
            except JsonBufferMaxAttempts:
                callback(None)
                return

    def resubscribe(self):
        """ Resubscribes for the event """
        try:
            self._handler.__mi_subscribe__(self.name,
                                           self.socket.sock_name,
                                           self.expire)
            self.last_subscription = time.time()
        except OpenSIPSEventException as e:
            raise e
        except OpenSIPSMIException as e:
            raise e

    def unsubscribe(self):
        """ Unsubscribes the event """
        try:
            self._handler.__mi_unsubscribe__(self.name, self.socket.sock_name)
            self.stop()
            del self._handler.events[self.name]
        except OpenSIPSEventException as e:
            raise e
        except OpenSIPSMIException as e:
            raise e

    def stop(self):
        """ Stops the current event processing """
        self.thread_stop.set()
        self.thread.join()
        self.socket.destroy()

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
