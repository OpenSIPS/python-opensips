from .connection import Connection
from . import jsonrpc_helper
import socket

class Datagram(Connection):
    def __init__(self, **kwargs):
        if "datagram_ip" not in kwargs:
            raise ValueError("datagram_ip is required for Datagram connector")
        
        if "datagram_port" not in kwargs:
            raise ValueError("datagram_port is required for Datagram connector")
        
        self.ip = kwargs["datagram_ip"]
        self.port = int(kwargs["datagram_port"])

    def execute(self, method: str, params: dict):
        jsoncmd = jsonrpc_helper.get_command(method, params)

        udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            udp_socket.sendto(jsoncmd.encode(), (self.ip, self.port))
            udp_socket.settimeout(5.0)
            reply = udp_socket.recv(32768)
        except Exception as e:
            raise jsonrpc_helper.JSONRPCException(e)
        finally:
            udp_socket.close()
        return jsonrpc_helper.get_reply(reply)
    
    def valid(self):
        return (True, None)
