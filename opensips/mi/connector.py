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

from abc import ABC, abstractmethod
import urllib.error
from . import jsonrpc_helper
import socket

import urllib.request
import urllib.parse
import ssl

import os
import time
import errno

class Connector(ABC):
    @abstractmethod
    def __init__(self, **kwargs):
        pass

    @abstractmethod
    def execute(self, method: str, params: dict):
        pass

    @abstractmethod
    def valid(self):
        pass

class Datagram(Connector):
    def __init__(self, **kwargs):
        if "ip" not in kwargs:
            raise ValueError("ip is required for Datagram connector")
        
        if "port" not in kwargs:
            raise ValueError("port is required for Datagram connector")
        
        self.ip = kwargs["ip"]
        self.port = kwargs["port"]

    def execute(self, method: str, params: dict):
        jsoncmd = jsonrpc_helper.get_command(method, params)
        udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            udp_socket.sendto(jsoncmd.encode(), (self.ip, self.port))
            udp_socket.settimeout(5.0)
            reply = udp_socket.recv(1024)
        except Exception as e:
            raise jsonrpc_helper.JSONRPCException(e)
        finally:
            udp_socket.close()
        return jsonrpc_helper.get_reply(reply)
    
    def valid(self):
        return (True, None)
    
class HTTP(Connector):
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
                reply = urllib.request.urlopen(request, context=ssl._create_unverified_context()).read().decode()
            else:
                reply = urllib.request.urlopen(request).read().decode()
        except urllib.error.HTTPError as e:
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
        except Exception as e:
            msg = "Could not connect to {} ({})".format(self.url, e)
            return (False, [msg, "Is OpenSIPS running?"])
    
class FIFO(Connector):
    REPLY_FIFO_FILE_TEMPLATE = "opensips_fifo_reply_{}_{}"\
    
    def __init__(self, **kwargs):
        if "fifo_file" not in kwargs:
            raise ValueError("fifo_file is required for FIFO connector")
        if "fifo_file_fallback" not in kwargs:
            raise ValueError("fifo_file_fallback is required for FIFO connector")
        if "fifo_reply_dir" not in kwargs:
            raise ValueError("fifo_reply_dir is required for FIFO connector")
        
        self.fifo_file = kwargs["fifo_file"]
        self.fifo_file_fallback = kwargs["fifo_file_fallback"]
        self.fifo_reply_dir = kwargs["fifo_reply_dir"]

    def execute(self, method: str, params: dict):
        jsoncmd = jsonrpc_helper.get_command(method, params)

        reply_fifo_file_name = self.REPLY_FIFO_FILE_TEMPLATE.format(os.getpid(), str(time.time()).replace(".", "_"))
        reply_fifo_file_path = os.path.join(self.fifo_reply_dir, reply_fifo_file_name)

        try:
            os.unlink(reply_fifo_file_path)
        except OSError as e:
            if os.path.exists(reply_fifo_file_path):
                raise jsonrpc_helper.JSONRPCException(
                    "Could not remove old reply FIFO file {}: {}"
                    .format(reply_fifo_file_path, e))
            
        try:
            os.mkfifo(reply_fifo_file_path)
            os.chmod(reply_fifo_file_path, 0o666)
        except OSError as e:
            raise jsonrpc_helper.JSONRPCException(
                "Could not create reply FIFO file {}: {}"
                .format(reply_fifo_file_path, e))
        
        if not os.path.exists(self.fifo_file):
            raise jsonrpc_helper.JSONRPCException(
                "FIFO file {} does not exist"
                .format(self.fifo_file))
        
        fifocmd = ":{}:{}".format(reply_fifo_file_path, jsoncmd)
        try:
            with open(self.fifo_file, "w") as fifo:
                fifo.write(fifocmd)
        except Exception as e:
            raise jsonrpc_helper.JSONRPCException(
                "Could not access FIFO file {}: {}"
                .format(self.fifo_file, e))
        
        reply = None
        try:
            with open(reply_fifo_file_path, "r") as reply_fifo:
                reply = reply_fifo.readline()
        except KeyboardInterrupt:
            exit()
        finally:
            os.unlink(reply_fifo_file_path)
            
        return jsonrpc_helper.get_reply(reply)
    
    def valid(self):
        opensips_fifo = self.fifo_file
        if not os.path.exists(opensips_fifo):
            opensips_fifo = self.fifo_file_fallback
            if not os.path.exists(opensips_fifo):
                return (False, ["FIFO file {} does not exist, nor does fallback file {}"
                                .format(self.fifo_file, self.fifo_file_fallback), "Is OpenSIPS running?"])
        try:
            open(opensips_fifo, "w").close()
        except OSError as e:
            extra = []
            if e.errno == errno.EACCES:
                sticky = self.get_sticky(os.path.dirname(opensips_fifo))
                if sticky:
                    extra = ["starting with Linux kernel 4.19, processes can " +
                            "no longer read from FIFO files ",
                            "that are saved in directories with sticky " +
                            "bits (such as {})".format(sticky),
                            "and are not owned by the same user the " +
                            "process runs with. ",
                            "To fix this, either store the file in a non-sticky " +
                            "bit directory (such as /var/run/opensips), ",
                            "or disable fifo file protection using " +
                            "'sysctl fs.protected_fifos=0' (NOT RECOMMENDED)"]
            msg = "Could not access FIFO file {}: {}".format(opensips_fifo, e)
            return (False, [msg] + extra)
        self.fifo_file = opensips_fifo
        return (True, None)
    
    def get_sticky(self, path):
        if path == "/":
            return None
        if os.stat(path).st_mode & 0o1000 == 0o1000:
            return path
        return self.get_sticky(os.path.split(path)[0])
