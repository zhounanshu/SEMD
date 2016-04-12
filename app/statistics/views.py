#!/usr/bin/env python
# -*- coding: utf-8 -*-
from ..models import *
from flask.ext.restful import Resource
import datetime
from ..lib.util import *


class totalData(Resource):
    def get(self):
        counts = devData.query.order_by('datatime desc').limit(1)[0]
        return {'status': 'success', 'data': counts.id}, 200


class eachDay(Resource):
    def get(self):
        end_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        start_time = end_time[:11] + '00:00:00'
        records = devData.query.filter(
            devData.datatime >= start_time,
            devData.datatime <= end_time).all()
        result = []
        if len(records) != 0:
            result = to_json_list(records)
        return {'status': 'success', 'data': result}, 200
