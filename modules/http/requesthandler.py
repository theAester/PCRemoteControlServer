from http.server import BaseHTTPRequestHandler, HTTPServer
from . import stateconsts as sc
import psutil
import socket
from os import path
import mimetypes as mt
import shutil

class HttpRequestHandler(BaseHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        self.state = kwargs.pop('mState', None)
        super().__init__(*args, **kwargs)


    def put_ips(self, temp, ips):
        ind = temp.index("%IPS%")
        before = temp[:ind]
        after = temp[(ind + 5):]
        return before + ips + after

    def put_key(self, temp, key):
        ind = temp.index("%KEY%")
        before = temp[:ind]
        after = temp[(ind + 5):]
        return before + key + after

    def put_info(self, temp, key, ips):
        return self.put_ips(self.put_key(temp, key), ips)
    
    # GET method
    def do_GET(self):
        print("BEGIN: ", self.path)
        if self.try_route_web(): return
        if self.path != "/":
            self.send_response(301)
            self.send_header("Location", "/")
            self.end_headers()
            return
        # Send response status code
        self.send_response(200)
        
        # Send headers
        self.send_header('Content-type','text/html')
        self.end_headers()

        
        match self.state['state']:
            case sc.STATE_BEGIN:
                #content = f'state 1 {self.state['key']} <br/> {self._get_ip_addresses()}'
                part = ""
                for ip in self._get_ip_addresses():
                    part += f"<li class=\"ip-addr\"><span class=\"mono-fmt\">{ip}</span></li>"
                with open("web/s1_template.html", 'r') as f:
                    template = f.read()
                    content = self.put_info(template, self.state['key'], part)
                    self.wfile.write(content.encode('utf-8'))

            case sc.STATE_CONNECTED:
                with open("s2_template.html", "r") as f:
                    shutil.copyfileobj(f, self.wfile)
        return

    def __call__(self):
        return self

    def try_route_web(self):
        BASE = "web/"
        ABS_BASE = path.abspath(BASE)
        abs_path = path.abspath(path.join(BASE, self.path[1:]))
        print("ATTEMPTED: ", abs_path, self.path)
        if not abs_path.startswith(ABS_BASE): return False
        if not path.exists(abs_path): 
            self.send_response(404)
            abs_path = "web/404.html"
        elif not path.isfile(abs_path):
            return False
        else:
            self.send_response(200)
        
        mime, _ = mt.guess_type(abs_path)
        if mime is None:
            mime = "application/octet-stream"
        self.send_header("Content-Type", mime)
        self.end_headers()
        with open(abs_path, 'rb') as f:
            shutil.copyfileobj(f, self.wfile)
        return True
        



    def _get_ip_addresses(self):
        ip_addresses = []
        
        for interface, addrs in psutil.net_if_addrs().items():
            for addr in addrs:
                if addr.family == socket.AF_INET:
                    ip_addresses.append(addr.address)
        
        return ip_addresses