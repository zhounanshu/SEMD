#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Blueprint
from flask.ext.restful import Api

Advice = Blueprint('Advice', __name__)
Advice_api = Api(Advice)

from .views import *
Advice_api.add_resource(sendMail, '/v1/mail')
