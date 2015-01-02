# -*- coding: utf-8 -*-

import falcon
from app.libs.hooks import serialize


@falcon.after(serialize)
class SignIn(object):
    def __init__(self, app):
        app.add_route('/account/signin', self)

    def on_post(self, req, resp):
        resp.status = falcon.HTTP_200
        resp.body = {'status': 'OK'}


@falcon.after(serialize)
class SignOut(object):
    def __init__(self, app):
        app.add_route('/account/signout', self)

    def on_get(self, req, resp):
        resp.status = falcon.HTTP_200
        resp.body = {'status': 'OK'}


@falcon.after(serialize)
class SignUp(object):
    def __init__(self, app):
        app.add_route('/account/signup', self)

    def on_post(self, req, resp):
        resp.status = falcon.HTTP_200
        resp.body = {'status': 'OK'}
