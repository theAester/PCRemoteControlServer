import webbrowser
from .httpserver import MyHttpServer
import time


def start_and_serve_http(port, mserver):
    signal = [True]
    http_server = MyHttpServer(port)
    mserver.start(signal)
    key = mserver.get_key()
    print("\n================== key ==================\n================= " + key + " ================")
    http_server.start(signal)
    http_server.set_display_key(key)
    mserver.set_connected_callback(http_server.set_connected)

    url = f"http://localhost:{port}/"

    webbrowser.open(url)

    try:
        while True:
            time.sleep(2)
    except KeyboardInterrupt:
        print("Interrupted")
        signal[0] = False
        http_server.shutdown()
        return


