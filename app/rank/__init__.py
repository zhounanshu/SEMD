#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Blueprint
from flask.ext.restful import Api

Ranks = Blueprint('Ranks', __name__)
ranks_api = Api(Ranks)

from .views import *
ranks_api.add_resource(countRank, '/v1/rank')
ranks_api.add_resource(get_bonus, '/v1/bouns')
ranks_api.add_resource(Rank, '/v1/get/rank')
ranks_api.add_resource(pageRank, '/v1/new/rank')
