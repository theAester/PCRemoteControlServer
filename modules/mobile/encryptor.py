import socket
import threading
import base64
from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2
from hashlib import sha256

class Encryptor:
    def __init__(self, password):
        self.ALGORITHM = "AES"
        self.TRANSFORMATION = "AES/CBC/PKCS5Padding"
        self.SALT = b'1234567812345678'  # Fixed salt for key generation
        self.ITERATION_COUNT = 65536
        self.KEY_LENGTH = 16  # 128 bits
        
        # Generate key from password
        #self.secret_key = PBKDF2(password, self.SALT, dkLen=self.KEY_LENGTH, count=self.ITERATION_COUNT)
        #print(self.secret_key)

        self.secret_key = sha256(password.encode("utf-8")).digest()[:16]
        print(self.secret_key)
        
        # Use a fixed IV (initialization vector)
        self.iv = self.SALT

    def encrypt(self, data):
        cipher = AES.new(self.secret_key, AES.MODE_CBC, self.iv)
        padded_data = self._pad(data)
        encrypted_bytes = cipher.encrypt(padded_data.encode('utf-8'))
        return base64.b64encode(encrypted_bytes).decode('utf-8')

    def decrypt(self, data):
        cipher = AES.new(self.secret_key, AES.MODE_CBC, self.iv)
        encrypted_bytes = base64.b64decode(data)
        decrypted_bytes = cipher.decrypt(encrypted_bytes)
        return self._unpad(decrypted_bytes.decode('utf-8'))

    def _pad(self, s):
        """PKCS5 padding to ensure that the input string length is a multiple of the block size (16 bytes)."""
        block_size = 16
        pad_num = block_size - len(s) % block_size
        return s + (chr(pad_num) * pad_num)

    def _unpad(self, s):
        """Remove PKCS5 padding."""
        pad_num = ord(s[-1])
        return s[:-pad_num]
