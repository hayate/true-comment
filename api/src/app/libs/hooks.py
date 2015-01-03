# -*- coding: utf-8 -*-

import falcon
import ujson as json


def serialize(req, resp):
    if isinstance(resp.body, dict):
        resp.body = json.dumps(resp.body)


def auth(req, resp, params):
    if 'user' not in req.env['session']:
        raise falcon.exceptions.HTTPUnauthorized("Invalid Session", "SignIn Required")
