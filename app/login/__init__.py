#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Blueprint
from flask.ext.restful import Api

Login = Blueprint('Login', __name__)
login_api = Api(Login)

from .views import *
login_api.add_resource(userView, '/v1/user/<id>')
login_api.add_resource(user, '/v1/user')
login_api.add_resource(verify_login, '/v1/login')
