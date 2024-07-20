from http.server import BaseHTTPRequestHandler, HTTPServer
from . import stateconsts as sc
import psutil
import socket

class HttpRequestHandler(BaseHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        self.state = kwargs.pop('mState', None)
        super().__init__(*args, **kwargs)
    
    # GET method
    def do_GET(self):
        # Send response status code
        self.send_response(200)
        
        # Send headers
        self.send_header('Content-type','text/html')
        self.end_headers()
        
        match self.state['state']:
            case sc.STATE_BEGIN:
                content = f'state 1 {self.state['key']} <br/> {self._get_ip_addresses()}'
            case sc.STATE_CONNECTED:
                content = 'state 2'
        
        # Write HTML content as response
        self.wfile.write(content.encode('utf-8'))
        return

    def __call__(self):
        return self


    def _get_ip_addresses(self):
        ip_addresses = []
        
        for interface, addrs in psutil.net_if_addrs().items():
            for addr in addrs:
                if addr.family == socket.AF_INET:
                    ip_addresses.append(addr.address)
        
        return ip_addresses