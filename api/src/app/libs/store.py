# -*- coding: utf-8 -*-

import redis
from config import Config
from psycopg2.extras import RealDictCursor
from psycopg2.pool import ThreadedConnectionPool


class Redis(object):
    __state = {}

    def __init__(self):
        self.__dict__ = self.__state
        if '_pool' not in self.__dict__:
            config = Config()
            params = {
                'db': config.redis['db'],
                'host': config.redis['host'],
                'port': config.redis['port']
            }
            self._pool = redis.ConnectionPool(**params)

        self._redis = redis.StrictRedis(connection_pool=self._pool)

    def __getattr__(self, name):
        return getattr(self._redis, name)


class Connection(object):
    """Database connection"""
    def __init__(self, conn):
        self.conn = conn

    def cursor(self):
        return self.conn.cursor(cursor_factory=RealDictCursor)

    def commit(self):
        self.conn.commit()

    def rollback(self):
        self.conn.rollback()


class Database(object):
    __state = {}

    def __init__(self, minconn=10, maxconn=100, **kwargs):
        self.__dict__ = self.__state
        if 'pool' not in self.__dict__:
            self.pool = ThreadedConnectionPool(minconn, maxconn, **kwargs)

    def getconn(self, key=None):
        return Connection(self.pool.getconn(key))

    def putconn(self, conn, key=None, close=False):
        self.pool.putconn(conn.conn, key, close)

    def closeall(self):
        return self.pool.closeall()
