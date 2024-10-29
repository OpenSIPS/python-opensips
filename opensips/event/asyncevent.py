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


""" Module that implements OpenSIPS Event behavior with asyncio """

import asyncio
from ..mi import OpenSIPSMIException
from .json_helper import JsonBuffer, JsonBufferMaxAttempts
from .event import OpenSIPSEventException


class AsyncOpenSIPSEvent():  # pylint: disable=too-many-instance-attributes

    """ Asyncio implementation of the OpenSIPS Event """

    def __init__(self, handler, name: str, callback, expire=None):
        self._handler = handler
        self.name = name
        self.callback = callback
        self.buf = JsonBuffer()
        if expire is not None:
            self.expire = expire
            self.reregister = False
        else:
            self.expire = 3600
            self.reregister = True

        try:
            self.socket = self._handler.__new_socket__()
            self.socket.create()
            self._handler.events[self.name] = self
            self.resubscribe_task = asyncio.create_task(self.resubscribe())
            loop = asyncio.get_running_loop()
            loop.add_reader(self.socket.sock.fileno(),
                            self.handle, self.callback)

        except ValueError as e:
            raise OpenSIPSEventException("Invalid arguments") from e

    def handle(self, callback):
        """ Handles the event callbacks """
        data = self.socket.read()
        if not data:
            return

        try:
            self.buf.push(data)
            while j := self.buf.pop():
                callback(j)
        except JsonBufferMaxAttempts:
            callback(None)
            return

    async def resubscribe(self):
        """ Resubscribes for the event """
        try:
            while True:
                try:
                    self._handler.__mi_subscribe__(self.name,
                                                   self.socket.sock_name,
                                                   self.expire)
                except OpenSIPSEventException:
                    return
                except OpenSIPSMIException:
                    return
                await asyncio.sleep(self.expire - 60)
                if not self.reregister:
                    break
        except asyncio.CancelledError:
            pass

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
        loop = asyncio.get_running_loop()
        loop.remove_reader(self.socket.sock.fileno())
        self.resubscribe_task.cancel()
        self.socket.destroy()
