#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask.ext.restful import Api
from flask import Blueprint

devMonitor = Blueprint('devMonitor', __name__)
dev_api = Api(devMonitor)

from .views import *
dev_api.add_resource(devResource, '/v1/device/data/upload')
dev_api.add_resource(usrResource, '/v1/user/data/upload')
dev_api.add_resource(reltiPerson, '/v1/device/person/realtime')
dev_api.add_resource(env_history, '/v1/device/history', '/v1/device/history/')
dev_api.add_resource(sportResource, '/v1/sport/data/upload')
