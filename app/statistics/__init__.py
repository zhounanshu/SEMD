#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask.ext.restful import Api
from flask import Blueprint
statist_blueprint = Blueprint('devStatist', __name__)
statist_api = Api(statist_blueprint)

from .views import *
statist_api.add_resource(totalData, '/v1/total/num')
