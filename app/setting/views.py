#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask.ext.restful import Resource
from flask.ext.restful import reqparse
from flask import request
from ..models import *
from ..lib.util import *


class viewSet(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('user_id', type=str)
        parser.add_argument('tempe_H', type=str)
        parser.add_argument('tempe_L', type=str)
        parser.add_argument('humi_H', type=str)
        parser.add_argument('humi_L', type=str)
        parser.add_argument('pressure_H', type=str)
        parser.add_argument('pressure_L', type=str)
        args = parser.parse_args(strict=True)
        user_id = args['user_id']
        user = User.query.filter_by(id=user_id).first()
        if user is None:
            return {'status': 'fail', 'mesg': '用户不存在!'}
        record = userSetting(user_id, args['tempe_H'],args['tempe_L'],args['humi_H'],
            args['humi_L'],args['pressure_H'], args['pressure_L'])
        db.session.add(record)
        try:
            db.session.commit()
            return {'status': 'success', 'mesg': '信息设置成功!'}
        except:
            return {'status': 'fail', 'mesg': '环境信息已经设置!'}
    def put(self):
        parser = reqparse.RequestParser()
        parser.add_argument('user_id', type=str)
        parser.add_argument('tempe_H', type=str)
        parser.add_argument('tempe_L', type=str)
        parser.add_argument('humi_H', type=str)
        parser.add_argument('humi_L', type=str)
        parser.add_argument('pressure_H', type=str)
        parser.add_argument('pressure_L', type=str)
        args = parser.parse_args(strict=True)
        user_id = args['user_id']
        record = userSetting.query.filter_by(user_id=user_id).first()
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
