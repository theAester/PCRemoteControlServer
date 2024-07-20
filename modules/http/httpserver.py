from http.server import BaseHTTPRequestHandler, HTTPServer
from .requesthandler import HttpRequestHandler
from .stateconsts import *
import threading as t


class MyHttpServer:
    def __init__(self, port):
        self.port=port
        self.state = {'state': STATE_BEGIN, 'key':''}
        self.thread = None

    def start(self, signal):
        self.signal = signal
        maker = lambda *args, **kwargs: HttpRequestHandler(*args, mState=self.state, **kwargs)
        self.server = HTTPServer(('127.0.0.1', self.port), maker)
        self.thread = t.Thread(target=self.server.serve_forever)
        self.thread.start();

    def set_display_key(self, key):
        self.state['key'] = key

    def set_connected(self):
        self.state['state'] = STATE_CONNECTED

    def join(self):
        if self.thread != None:
            self.thread.join()

    def shutdown(self):
        self.server.shutdown()