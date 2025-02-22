#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "Christophe Druet"
__copyright__ = "Copyright (c) 2022-YYYY ENTSO-E - All rights reserved."
__credits__ = ['Christophe Druet']
__maintainer__ = "Christophe Druet"
__email__ = "christophe.druet@entsoe.eu"

from typing import Any, Dict


class Encryptor:
    def encrypt(self, data: Dict[str, Any]) -> str:
        pass

    def decrypt(self, encrypted_data: str) -> Dict[str, Any]:
        pass
