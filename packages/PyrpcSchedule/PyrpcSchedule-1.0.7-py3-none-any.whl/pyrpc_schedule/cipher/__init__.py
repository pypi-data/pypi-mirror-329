# -*- encoding: utf-8 -*-

class Cipher:
    """
    A class for decrypting ciphertext using an RSA private key.

    This class takes a configuration dictionary containing ciphertext and a private key,
    decodes them from base64 to bytes, and provides a method to decrypt the ciphertext using the RSA private key.

    """
    _config = None

    def __init__(self, config):
        """
        Initialize the _Cipher class.

        Args:
            config (dict): A dictionary containing the ciphertext and private key.
            The keys are defined by CIPHER_CIPHERTEXT_KEY and CIPHER_PRIVATE_KEY_KEY.
        """
        self._config = config

    def initialize(self):
        """
        Initialize the _Cipher class.
        """

    def cipher_rsa_dec(self):
        """
        Decrypt the ciphertext using the RSA private key.

        Returns:
            bytes: The decrypted plaintext.
        """
