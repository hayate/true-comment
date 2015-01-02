# -*- coding: utf-8 -*-

import os
import falcon
import pkgutil
import inspect
from libs.config import Config
from libs.store import Database
try:
    from ConfigParser import SafeConfigParser
except ImportError:
    from configparser import SafeConfigParser


class App(object):
    __state = {}

    def __init__(self, filepath):
        """api wsgi main class

        filepath -- fullpath to config.ini file
        """
        self.__dict__ = self.__state
        if 'app' not in self.__dict__:
            conf = SafeConfigParser()
            conf.read(filepath)
            # initialize global config
            config = Config(conf)
            self.app = falcon.API()
            self.load_routes()
            db = {'database': config['database']['name'],
                  'user': config['database']['user']}
            minconn = config['database']['minconn']
            maxconn = config['database']['maxconn']
            self.database = Database(minconn, maxconn, **db)

    def load_routes(self):
        """load routes here"""
        path = os.path.dirname(os.path.realpath(__file__))
        controllers = os.path.join(path, 'controllers')
        for _, name, _ in pkgutil.iter_modules([controllers]):
            module_name = 'app.controllers.{0}'.format(name)
            module = __import__(module_name, fromlist=[name])
            clss = inspect.getmembers(module, inspect.isclass)
            for cls in clss:
                cls[1](self.app)

    def __call__(self, environ, start_response):
        environ['PATH_INFO'] = environ['PATH_INFO'].rstrip('/')
        if self.database is not None:
            environ['db_conn'] = self.database.getconn()

        def middleware_start_response(status, response_headers, exc_info=None):
            if self.database is not None:
                self.database.putconn(environ['db_conn'])
            return start_response(status, response_headers, exc_info)
        return self.app(environ, middleware_start_response)
