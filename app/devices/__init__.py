#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Blueprint
from flask.ext.restful import Api

Device = Blueprint('Device', __name__)
device_api = Api(Device)

from .views import *
device_api.add_resource(devResource, '/v1/device')
