from .connection import Connection
import urllib.error
from . import jsonrpc_helper
import socket

import urllib.request
import urllib.parse
import ssl

class HTTP(Connection):
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
