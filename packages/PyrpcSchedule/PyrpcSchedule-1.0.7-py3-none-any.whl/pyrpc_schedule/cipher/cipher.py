# -*- encoding: utf-8 -*-

import base64
from Cryptodome.PublicKey import RSA
from Cryptodome.Cipher import PKCS1_v1_5

from pyrpc_schedule.meta import CIPHER_CIPHERTEXT_KEY, CIPHER_PRIVATE_KEY_KEY
from pyrpc_schedule.cipher import Cipher


class _Cipher:
    """
    A class for decrypting ciphertext using an RSA private key.

    This class takes a configuration dictionary containing ciphertext and a private key,
    decodes them from base64 to bytes, and provides a method to decrypt the ciphertext using the RSA private key.

    """

    _instance = None
    _interface = Cipher

    _config = None
    _ciphertext = None
    _private_key = None

    def __new__(cls, *args, **kwargs):
        for name, func in cls.__dict__.items():
            if not name.startswith("__") and not name.endswith("__"):
                setattr(cls._interface, name, func)

        return super().__new__(cls)

    def initialize(self):
        """
        Initialize the _Cipher class.
        """
        self._ciphertext = base64.b64decode(self._config[CIPHER_CIPHERTEXT_KEY].encode('utf-8'))
        self._private_key = base64.b64decode(self._config[CIPHER_PRIVATE_KEY_KEY].encode('utf-8'))

    def cipher_rsa_dec(self):
        """
        Decrypt the ciphertext using the RSA private key.

        Returns:
            bytes: The decrypted plaintext.
        """

        key = RSA.import_key(self._private_key)
        cipher = PKCS1_v1_5.new(key)
        return cipher.decrypt(self._ciphertext, None)


_Cipher()
