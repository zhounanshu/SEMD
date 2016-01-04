#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Blueprint
from flask.ext.restful import Api

Friends = Blueprint('Friends', __name__)
friends_api = Api(Friends)

from .views import *
friends_api.add_resource(friend, '/v1/friend')
friends_api.add_resource(searchFriend, '/v1/search/friend')
