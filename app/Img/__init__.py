#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Blueprint
from flask.ext.restful import Api

imgBlueprint = Blueprint('imgBlueprint', __name__)
img_api = Api(imgBlueprint)

from .views import *
img_api.add_resource(imgResource, '/v1/img/<id>')
