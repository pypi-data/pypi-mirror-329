import json
from base64 import b64decode, b64encode
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
from Osdental.Exception.ControlledException import RSAEncryptException
from Osdental.Utils.Message import UNEXPECTED_ERROR
from Osdental.Utils.Constant import CHARSET
from Osdental.Utils.Code import APP_ERROR

class RSAEncryptor:

    @staticmethod
    def encrypt(data: str | dict, public_key_rsa: str) -> str:
        try:
            if isinstance(data, dict):
                data = json.dumps(data)

            public_key = serialization.load_pem_public_key(public_key_rsa.encode(CHARSET))
            data_bytes = data.encode(CHARSET)
            encrypted_bytes = public_key.encrypt(
                data_bytes,
                padding.OAEP(
                    mgf=padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label=None
                )
            )

            return b64encode(encrypted_bytes).decode(CHARSET)

        except Exception as e:
            raise RSAEncryptException(message=UNEXPECTED_ERROR, error=str(e), status_code=APP_ERROR) 


    @staticmethod
    def decrypt(data: str, private_key_rsa: str) -> str:
        try:
            encrypted_bytes = b64decode(data)
            private_key = serialization.load_pem_private_key(private_key_rsa.encode(CHARSET), password=None)
            decrypted_bytes = private_key.decrypt(
                encrypted_bytes,
                padding.OAEP(
                    mgf=padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label=None
                )
            )

            return decrypted_bytes.decode(CHARSET)

        except Exception as e:
            raise RSAEncryptException(message=UNEXPECTED_ERROR, error=str(e), status_code=APP_ERROR)