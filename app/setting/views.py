#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask.ext.restful import Resource
from flask.ext.restful import reqparse
from flask import request
from ..models import *
from ..lib.util import *


class viewSet(Resource):
    def put(self, id):
        parser = reqparse.RequestParser()
        parser.add_argument('tempe_H', type=str)
        parser.add_argument('tempe_L', type=str)
        parser.add_argument('humi_H', type=str)
        parser.add_argument('humi_L', type=str)
        parser.add_argument('pressure_H', type=str)
        parser.add_argument('pressure_L', type=str)
        args = parser.parse_args(strict=True)
        record = userSetting.query.filter_by(user_id=id).first()
        if record is None:
            return {'status': 'fail', 'mesg': '用户不存在!'}
        record.tempe_H = args['tempe_H']
        record.tempe_L = args['tempe_L']
        record.humi_L = args['humi_L']
        record.humi_H = args['humi_H']
        record.pressure_H = args['pressure_H']
        record.pressure_L = args['pressure_L']
        try:
            db.session.commit()
            return {'status': 'success', 'mesg': '信息更新成功!'}
        except:
            return {'status': 'fail', 'mesg': '信息更新失败!'}
