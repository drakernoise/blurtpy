# -*- coding: utf-8 -*-
import hashlib
import base64
try:
    from Cryptodome import Random
    from Cryptodome.Cipher import AES
except ImportError:
    try:
        from Crypto import Random
        from Crypto.Cipher import AES
    except ImportError:
        raise ImportError("Missing dependency: pyCryptodome")


class AESCipher(object):
    """
    A classical AES Cipher. Can use any size of data and any size of password thanks to padding.
    Also ensure the coherence and the type of the data with a unicode to byte converter.
    """
    def __init__(self, pass_secret):
        self.bs = 32
        # SHA256 is used here as a simple key derivation from a passphrase string.
        self.h_key = hashlib.new('sha256', AESCipher.str_to_bytes(pass_secret)).digest()  # lgtm [py/weak-password-hashing] # codeql [py/weak-password-hashing] # codeql[py/weak-password-hashing]
    
    @property
    def key(self):
        """Backwards compatibility property for accessing the hashed key."""
        return self.h_key
    
    @key.setter
    def key(self, value):
        """Backwards compatibility property setter."""
        self.h_key = value

    @staticmethod
    def str_to_bytes(data):
        u_type = type(b''.decode('utf8'))
        if isinstance(data, u_type):
            return data.encode('utf8')
        return data

    def _pad(self, s):
        return s + (self.bs - len(s) % self.bs) * AESCipher.str_to_bytes(chr(self.bs - len(s) % self.bs))

    @staticmethod
    def _unpad(s):
        return s[:-ord(s[len(s) - 1:])]

    def encrypt(self, raw):
        raw = self._pad(AESCipher.str_to_bytes(raw))
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(self.h_key, AES.MODE_CBC, iv)
        return base64.b64encode(iv + cipher.encrypt(raw)).decode('utf-8')

    def decrypt(self, enc):
        enc = base64.b64decode(enc)
        iv = enc[:AES.block_size]
        cipher = AES.new(self.h_key, AES.MODE_CBC, iv)
        return self._unpad(cipher.decrypt(enc[AES.block_size:])).decode('utf-8')
