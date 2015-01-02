# -*- coding: utf-8 -*-

import uuid
import hashlib
import binascii
import ujson as json
from store import Redis

import wsgisession

from crypto import Crypto
from config import Config
from logger import Logger


class Session(wsgisession.Session):

    def get_delete(self, key, default=None):
        value = self.get(key, default)
        try:
            del self[key]
        except KeyError:
            pass
        return value


class SessionFactory(object):

    def __init__(self):
        self.config = Config()
        self.crypto = Crypto()
        self.environ = {}
        self.redis = Redis()
        self.log = Logger.get()

    def load(self, id):
        try:
            session = Session()
            if id is not None:
                try:
                    dec = self.crypto.decrypt(id)
                except Exception as e:
                    self.log.exception(e)
                    dummy = uuid.uuid4().bytes
                    dec = ''.join([dummy, dummy])
                client_data, key = (dec[:16], binascii.hexlify(dec[16:]))
                if client_data != self.client_data():
                    self.redis.delete(key)
                    session.id = uuid.uuid4().hex
                else:
                    try:
                        session.data = json.loads(self.redis.get(key))
                    except (ValueError, TypeError) as e:
                        self.log.debug(e)
                        session.data = {}
                    session.id = key
            else:
                session.id = uuid.uuid4().hex
            return session
        except Exception as e:
            self.log.exception(e)
            if session.id is None:
                session.id = uuid.uuid4().hex
            return session

    def save(self, session):
        try:
            if session is not None:
                key = session.id
                try:
                    ttl = self.redis.ttl(key)
                    self.redis.set(key, json.dumps(session.data))
                    if ttl < 0:
                        ttl = self.config.redis['expires']
                    self.redis.expire(key, ttl)
                except TypeError as e:
                    self.log.exception(e)
                return self.crypto.encrypt(''.join([self.client_data(),
                                                    binascii.unhexlify(key)]))
        except Exception as e:
            self.log.exception(e)

    def client_data(self):
        try:
            ip = self.environ.get('REMOTE_ADDR',
                                  self.environ['HTTP_X_FORWARDED_FOR'])
        except KeyError:
            ip = '127.0.0.1'
            Logger.get().error("Could not find REMOTE_ADDR using: {0}".format(ip))
        try:
            user_agent = self.environ['HTTP_USER_AGENT']
        except KeyError:
            user_agent = 'Unknown'
            Logger.get().error("Could not find HTTP_USER_AGENT using: {0}".format(user_agent))
        return hashlib.md5(''.join([ip, user_agent])).digest()


class SessionMiddleware(wsgisession.SessionMiddleware):

    def __init__(self, app, factory):
        config = Config()
        cookie_key = config.session.get('cookie_key', 'session_id')
        env_key = config.session.get('env_key', 'session')
        super(SessionMiddleware, self).__init__(app, factory, env_key,
                                                cookie_key)

    def __call__(self, environ, start_response):
        self.factory.environ = environ
        return super(SessionMiddleware, self).__call__(environ, start_response)
