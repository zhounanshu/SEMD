#!/usr/bin/env python
# -*- coding: utf-8 -*-
from ..models import *
from flask.ext.restful import Resource
from ..lib.util import *


class totalData(Resource):
    def get(self):
        counts = devData.query.order_by('datatime desc').limit(1)[0]
        return {'status': 'success', 'data': counts.id}, 200
