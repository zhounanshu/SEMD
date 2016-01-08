#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Blueprint
from flask.ext.restful import Api

userSet = Blueprint('userSet', __name__)
set_api = Api(userSet)

from .views import *
set_api.add_resource(viewSet, '/v1/user/setting')
set_api.add_resource(feed, '/v1/user/feed')
