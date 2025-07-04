from typing import Optional

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes


private_key = rsa.generate_private_key(public_exponent=65537, key_size=8192, backend=default_backend())
public_key = private_key.public_key()


def encrypt(data: str) -> bytes:
    return public_key.encrypt(data.encode(), padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None))


def decrypt(data: bytes) -> Optional[str]:
    try:
        return private_key.decrypt(data, padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None)).decode()
    except:
        return None 
