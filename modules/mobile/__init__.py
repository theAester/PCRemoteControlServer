from .mobileserver import MobileServer

def create_mobile_server(port, wrapper):
    return MobileServer(port, wrapper)