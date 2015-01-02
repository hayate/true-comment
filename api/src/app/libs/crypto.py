# -*- coding: utf-8 -*-

import uuid
import base64
import binascii

from Crypto.Cipher import AES

from config import Config


class Crypto(object):
    __state = {}

    def __init__(self):
        self.__dict__ = self.__state
        if 'key' not in self.__dict__:
            config = Config()
            self.key = binascii.unhexlify(config.main['secret_key'])

    def encrypt(self, data):
        iv = uuid.uuid4().bytes
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return base64.b64encode(''.join([iv, cipher.encrypt(data)]))

    def decrypt(self, data):
        data = base64.b64decode(data)
        iv = data[:16]
        data = data[16:]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return cipher.decrypt(data)
