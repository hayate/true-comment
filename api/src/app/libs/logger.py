# -*- coding: utf-8 -*-

import sys
import logging
from config import Config
from logging.handlers import RotatingFileHandler


class Logger(object):
    __state = {}

    def __init__(self):
        self.__dict__ = self.__state
        if '_log' not in self.__dict__:
            try:
                config = Config()
                handler = RotatingFileHandler(config.logger['filepath'],
                                              maxBytes=config.logger['max_bytes'],
                                              backupCount=5, encoding='UTF-8')
                formatter = logging.Formatter('%(levelname)s - %(asctime)s - ' +
                                              'File:%(pathname)s - Line:' +
                                              '%(lineno)d - Func:' +
                                              '%(funcName)s\n%(message)s')

                level = int(config.logger['level'])
                handler.setLevel(level)
                handler.setFormatter(formatter)
                self._log = logging.getLogger(__name__)
                self._log.setLevel(level)
                self._log.addHandler(handler)
            except IOError as e:
                print("Could not initialize Logger: {0}".format(e))
                sys.exit()

    def __call__(self):
        return self._log

    @classmethod
    def get(cls):
        if isinstance(cls, Logger):
            return cls()
        return cls()()
