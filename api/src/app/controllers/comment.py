# -*- coding: utf-8 -*-

import falcon
from app.libs.hooks import auth
from app.libs.hooks import serialize


@falcon.before(auth)
@falcon.after(serialize)
class List(object):
    def __init__(self, app):
        app.add_route('/comment/list', self)

    def on_get(self, req, resp):
        resp.status = falcon.HTTP_200
        resp.body = {'status': 'OK'}
