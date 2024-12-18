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

""" HTTP implementation of MI """

import ssl
import socket
import urllib.error
import urllib.parse
import urllib.request
from .connection import Connection
from . import jsonrpc_helper


class HTTP(Connection):

    """ HTTP communication socket """

    def __init__(self, **kwargs):
        if "url" not in kwargs:
            raise ValueError("url is required for HTTP connector")

        self.url = kwargs["url"]

    def execute(self, method: str, params: dict):
        jsoncmd = jsonrpc_helper.get_command(method, params)
        headers = {
            "Content-Type": "application/json"
        }
        request = urllib.request.Request(self.url, jsoncmd.encode(), headers)
        url_parsed = urllib.parse.urlparse(self.url)
        try:
            if url_parsed.scheme == "https":
                # pylint: disable=protected-access
                ssl_ctx = ssl._create_unverified_context()
            else:
                ssl_ctx = None
            with urllib.request.urlopen(request, context=ssl_ctx) as rpl:
                reply = rpl.read().decode()
        except Exception as e:  # pylint: disable=broad-exception-caught
            raise jsonrpc_helper.JSONRPCException(str(e))
        return jsonrpc_helper.get_reply(reply)

    def valid(self):
        try:
            url_parsed = urllib.parse.urlparse(self.url)
            if not url_parsed.port:
                if url_parsed.scheme == "http":
                    url_parsed.port = 80
                else:
                    url_parsed.port = 443
            sock = socket.socket()
            sock.connect((url_parsed.hostname, url_parsed.port))
            sock.close()
            return (True, None)
        except Exception as e:  # pylint: disable=broad-exception-caught
            msg = f"Could not connect to {self.url} ({e})"
            return (False, [msg, "Is OpenSIPS running?"])

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
