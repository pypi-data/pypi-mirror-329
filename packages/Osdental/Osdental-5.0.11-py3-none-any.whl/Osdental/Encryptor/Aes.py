import os
import json
import base64
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from Osdental.Exception.ControlledException import AESEncryptException
from Osdental.Utils.Message import UNEXPECTED_ERROR
from Osdental.Utils.Constant import CHARSET
from Osdental.Utils.Code import APP_ERROR

class AES:

    def __init__(self):
        self.IV_LENGTH = 32
        self.TAG_LENGTH = 16

    @staticmethod
    def generate_key() -> str:
        """Generates a random 256-bit AES key and returns it Base64 encoded."""
        key = os.urandom(32)
        return base64.b64encode(key).decode(CHARSET)
    
    def encrypt(self, aes_key: str, data: dict | str | list) -> str:
        """
        Encrypts data using AES-GCM.
        Supports dictionary, string, or list inputs.

        :param aes_key: AES key in Base64 format.
        :param data: Data to be encrypted (dict, str, or list).
        :return: Data encrypted in Base64.
        """
        if not isinstance(data, (dict, str, list)):
            raise ValueError(AES_INPUT)

        try:
            key = base64.b64decode(aes_key)
            iv = os.urandom(self.IV_LENGTH)
            if isinstance(data, (dict, list)):
                json_data = json.dumps(data)
            else:
                json_data = data

            cipher = Cipher(algorithms.AES(key), modes.GCM(iv))
            encryptor = cipher.encryptor()
            ciphertext = encryptor.update(json_data.encode(CHARSET)) + encryptor.finalize()
            tag = encryptor.tag
            encrypted_data = iv + ciphertext + tag

            return base64.b64encode(encrypted_data).decode(CHARSET)

        except Exception as e:
            raise AESEncryptException(message=UNEXPECTED_ERROR, error=str(e), status_code=APP_ERROR)
 

    def decrypt(self, aes_key: str, encrypted_data: str):
        """
        Decrypts data using AES-GCM.
        Expects encrypted data to represent either a JSON object (dict) or a plain string.

        :param aes_key: AES key in Base64 format.
        :param encrypted_data: Data encrypted in Base64.
        :return: Decrypted data (either dict or str).
        """
        try:
            key = base64.b64decode(aes_key)
            encrypted_data = base64.b64decode(encrypted_data)
            iv = encrypted_data[:self.IV_LENGTH]
            tag = encrypted_data[-self.TAG_LENGTH:]
            ciphertext = encrypted_data[self.IV_LENGTH:-self.TAG_LENGTH]
            cipher = Cipher(algorithms.AES(key), modes.GCM(iv, tag))
            decryptor = cipher.decryptor()
            plaintext = decryptor.update(ciphertext) + decryptor.finalize()

            try:
                decrypted_data = json.loads(plaintext.decode(CHARSET))
                return decrypted_data
            except json.JSONDecodeError:
                return plaintext.decode(CHARSET)

        except Exception as e:
            raise AESEncryptException(message=UNEXPECTED_ERROR, error=str(e), status_code=APP_ERROR)