
from modules.mobile import create_mobile_server
from modules.ui_wrapper import get_ui_wrapper
from modules.http import start_and_serve_http

MOBILE_PORT=25881
HTTP_PORT=25880

def main():
    ui_wrapper = get_ui_wrapper()
    mobile_server = create_mobile_server(MOBILE_PORT, ui_wrapper)
    http_server = start_and_serve_http(HTTP_PORT, mobile_server)


if __name__ == "__main__":
    main()