#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "Christophe Druet"
__copyright__ = "Copyright (c) 2022-YYYY ENTSO-E - All rights reserved."
__credits__ = ['Christophe Druet']
__maintainer__ = "Christophe Druet"
__email__ = "christophe.druet@entsoe.eu"

import os
import json
import zlib
import base64
from typing import Any, Dict

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from ez_credentials import TokenManager
from loguru import logger

from .base import Encryptor


class CompressAndEncryptIt(Encryptor):
    def __init__(self, data_collection: str):
        """
        Initialize the Encryptor class with TokenManager for key management.
        
        :param data_collection: The data collection name for TokenManager.
        """
        service_name = f'pemmdb-store-{data_collection}'
        self.__token_manager = TokenManager(service_name, expires_in=None)

        self.__token = None

    def is_token_set(self):
        return self.__token_manager.token is not None

    def is_token_valid(self):
        return self.__token is not None and len(self.__token) == 32

    def _get_token(self):
        if self.is_token_valid():
            return self.__token

        self.__token = base64.b64decode(self.__token_manager.token)

        # Validate that the token is valid for AES-256
        if len(self.__token) != 32:
            logger.warning("Invalid token size for AES-256. Generating a new one.")
            self.__token_manager.token = base64.b64encode(os.urandom(32)).decode('utf-8')
            self.__token = base64.b64decode(self.__token_manager.token)

        return self.__token

    def encrypt(self, data: str | Dict[str, Any]) -> str:
        """
        Encrypts and compresses a JSON string.
        
        :param data: The data to encrypt and compress.
        :return: A base64-encoded string of the IV and encrypted data.
        """
        # Convert JSON to string and then to bytes
        json_str = json.dumps(data) if isinstance(data, dict) else data
        json_bytes = json_str.encode("utf-8")

        # Compress the data
        compressed_data = zlib.compress(json_bytes)

        # Generate random initialization vector
        iv = os.urandom(16)  # AES IV

        # Encrypt the compressed data
        try:
            cipher = Cipher(algorithms.AES(self._get_token()), modes.CBC(iv), backend=default_backend())
            encryptor = cipher.encryptor()

            # Add padding
            padder = padding.PKCS7(algorithms.AES.block_size).padder()
            padded_data = padder.update(compressed_data) + padder.finalize()

            encrypted_data = encryptor.update(padded_data) + encryptor.finalize()

            # Combine IV and encrypted data
            result = base64.b64encode(iv + encrypted_data).decode("utf-8")

        except ValueError as e:
            if str(e).startswith('Invalid key size'):
                self.__token_manager.renew_token()
            
            raise e

        return result

    def decrypt(self, encrypted_data: str) -> Dict[str, Any]:
        """
        Decrypts and decompresses a base64-encoded string of encrypted data.
        
        :param encrypted_data: The base64-encoded encrypted and compressed data.
        :return: The original JSON data as a dictionary.
        """
        try:
            # Decode the base64-encoded string
            encrypted_bytes = base64.b64decode(encrypted_data)

            # Extract IV and encrypted data
            iv = encrypted_bytes[:16]  # AES block size
            encrypted_payload = encrypted_bytes[16:]

            # Decrypt the data
            cipher = Cipher(algorithms.AES(self._get_token()), modes.CBC(iv), backend=default_backend())
            decryptor = cipher.decryptor()
            padded_data = decryptor.update(encrypted_payload) + decryptor.finalize()

            # Remove padding
            unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
            compressed_data = unpadder.update(padded_data) + unpadder.finalize()

            # Decompress the data
            json_bytes = zlib.decompress(compressed_data)
            json_str = json_bytes.decode("utf-8")

            # Convert JSON string back to dictionary
            data = json.loads(json_str)

        except ValueError as e:
            if str(e).startswith('Invalid key size'):
                self.__token_manager.renew_token()

            raise e

        return data
