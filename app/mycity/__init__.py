#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask.ext.restful import Api
from flask import Blueprint
myCity_blueprint = Blueprint('myCity', __name__)
mycity_api = Api(myCity_blueprint)

from .views import *
mycity_api.add_resource(reltiPeople, '/v1/map/view/device')
