#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Blueprint
from flask.ext.restful import Api

Friends = Blueprint('Friends', __name__)
friends_api = Api(Friends)

from .views import *
friends_api.add_resource(friend, '/v1/friend')
friends_api.add_resource(searchFriend, '/v1/search/friend')
friends_api.add_resource(searchFrid, '/v1/query/freind')
friends_api.add_resource(usrApply, '/v1/apply/freind')
friends_api.add_resource(approv, '/v1/approved/freind')
friends_api.add_resource(friendInfor, '/v1/get/freinds')
