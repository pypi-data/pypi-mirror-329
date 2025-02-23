"""
Secure Network - A simple way to authorize and share internet connections.

Ever wanted a easy, secure, and efficient way to share data between 
one device and the other? Well, now you can! In fact, it's super 
easy with our server and client architectures. Give it a try!

VERSION 1.0.0
BY Neo Zetterberg (From sweden)
"""

from .authenticator import SERVER, CLIENT, AuthSocket
from .network import SecureMessage, simple_socket, Event, EventType, Server, Client, generate_key, generate_hmac_key

import hashlib
import base64

def hkdf_expand(seed: bytes, length: int, salt: bytes = b"keygen_salt") -> bytes:
    """Derives a cryptographic key of the given length using HKDF."""
    key_material = hashlib.pbkdf2_hmac('sha256', seed, salt, iterations=100000, dklen=length)
    return key_material

def keys_from_passphrase(passphrase: str) -> tuple[bytes, bytes]:
    """
    Generates raw byte keys from a passphrase and allows reversibility.
    
    First one is the fernet key, and the second one is the HMAC key.
    """
    seed = hashlib.sha256(passphrase.encode()).digest() # Stable seed

    fernet_key_raw = hkdf_expand(seed, 32, salt=b"fernet_salt") # 32-byte raw Fernet key
    hmac_key_raw = hkdf_expand(seed, 64, salt=b"hmac_salt") # 64-byte raw HMAC key

    fernet_key = base64.urlsafe_b64encode(fernet_key_raw) # Fernet keys should be Base64 encoded

    return fernet_key, hmac_key_raw

def passphrase_from_keys(fernet_key: bytes, hmac_key: bytes) -> str:
    """
    Reconstructs the passphrase from the keys using the original derivation method.
    
    Be aware that it can only return a optionate passphrase, the original is lost if not 
    perserved from keys creation.
    """
    fernet_key_raw = base64.urlsafe_b64decode(fernet_key) # Decode to raw bytes

    combined_seed = hashlib.sha256(fernet_key_raw + hmac_key).digest()
    passphrase = hashlib.sha256(combined_seed).hexdigest() # Convert back to a string

    return passphrase