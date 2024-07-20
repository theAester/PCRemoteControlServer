import random
import socket
import threading
from .encryptor import Encryptor
from .actions import Actions


class MobileServer:
    def __init__(self, port, wrapper):
        self.port=port
        self.actions = Actions(wrapper)
        self.callback = lambda _: None
        self.recv_callback = lambda _: None
        self.key = self._gen_key()
        self.encryptor = Encryptor(self.key)

    def start(self, signal):
        self.signal = signal
        return self._listen("0.0.0.0", self.key)

    def _listen(self, address, key):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((address, self.port))
        self.server_socket.settimeout(1)
        self.server_socket.listen() 

        self.listen_thread = threading.Thread(target=self._accept_client)
        self.listen_thread.start()

    def join(self):
        if self.listen_thread != None:
            self.listen_thread.join()

    def get_key(self):
        return self.key

    def set_recv_callback(self, callback):
        self.recv_callback = callback

    def set_connected_callback(self, callback):
        self.callback=callback

    def _gen_key(self):
        s = ""
        for _ in range(8):
            s += random.choice("1234567890abcdefghijklmnopqrstuvwxyz")
        return s

    def _accept_client(self):
        while self.signal[0]:
            try: 
                self.client_socket, client_address = self.server_socket.accept()
            except TimeoutError:
                continue
            print(f"Connection accepted from {client_address}")
            if self._perform_handshake():
                self._handle_client()
        print("Skipping")

    def _perform_handshake(self):
        try:
            self.client_socket.sendall((self.encryptor.encrypt("HANDSHAKE") + "\n").encode('utf-8'))
            print("Handshake sent")
            response = self.client_socket.recv(1024).decode().strip()
            if self.encryptor.decrypt(response) == "HANDSHAKE":
                print("Handshake successful")
                return True
            else:
                print("Handshake failed")
                self.client_socket.close()
                self.client_socket = None
                return False
        except Exception as e:
            print(f"Handshake error: {e}")
            self.client_socket.close()
            self.client_socket = None
            return False

    def _handle_client(self):
        self.callback()
        try:
            buffer = bytearray()
            self.client_socket.settimeout(0.01)
            while self.signal[0]:
                try:
                    data = self.client_socket.recv(1024)
                except TimeoutError:
                    continue
                except ConnectionResetError:
                    break
                if not data:
                    break
                buffer.extend(data)


                # Split received data into lines
                while b"\n" in buffer:
                    idx = buffer.index(b"\n")
                    encrypted_message = buffer[:idx].decode('utf-8').strip()
                    del buffer[:idx+1]

                    # Decrypt and handle the message
                    decrypted_message = self.encryptor.decrypt(encrypted_message)
                    self.actions.handle_action(decrypted_message)
                    if self.recv_callback:
                        self.recv_callback(decrypted_message)
            print("ending")

        except Exception as e:
            print(f"Error: {e}")
        finally:
            self.client_socket.close()
            self.client_socket = None

    def send(self, message):
        try:
            if self.client_socket:
                encrypted_message = self.encryptor.encrypt(message)
                self.client_socket.sendall((encrypted_message + "\n").encode('utf-8'))
        except Exception as e:
            print(f"Error sending message: {e}")

    def disconnect(self):
        if self.client_socket:
            self.client_socket.close()
            self.client_socket = None
        if self.server_socket:
            self.server_socket.close()
            self.server_socket = None 
