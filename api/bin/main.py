#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
# path to configuration file
filepath = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                        'config.ini')
from app.app import App
from app.libs.session import SessionFactory
from app.libs.session import SessionMiddleware
application = SessionMiddleware(App(filepath), SessionFactory())
