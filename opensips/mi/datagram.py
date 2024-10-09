from .connection import Connection
from . import jsonrpc_helper
import socket

class Datagram(Connection):
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
