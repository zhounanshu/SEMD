#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask.ext.restful import Resource
from flask.ext.restful import reqparse
from flask import request
import datetime
from ..models import *
from ..lib.util import *


class devResource(Resource):

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('datatime', type=str)
        parser.add_argument('device_mac', type=str)
        parser.add_argument('user_id', type=str)
        parser.add_argument('longitude', type=str)
        parser.add_argument('latitude', type=str)
        parser.add_argument('temperature', type=str)
        parser.add_argument('humidity', type=str)
        parser.add_argument('pressure', type=str)
        parser.add_argument('uvIndex', type=str)
        args = parser.parse_args(strict=True)
        record = devData(args['datatime'], args['device_mac'],
                         args['user_id'], args['longitude'], args['latitude'],
                         args['temperature'], args['humidity'],
                         args['pressure'], args['uvIndex'])
        try:
            db.session.add(record)
            db.session.commit()
            return {'mesg': '数据上传成功!'}, 200
        except:
            return {'mesg': '数据上传失败!'}, 400


class usrResource(Resource):

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('datatime', type=str)
        parser.add_argument('user_id', type=str)
        parser.add_argument('weather')
        parser.add_argument('tempe', type=str)
        parser.add_argument('humi', type=str)
        parser.add_argument('pressure', type=str)
        parser.add_argument('uvIndex', type=str)
        parser.add_argument('longitude', type=str)
        parser.add_argument('latitude', type=str)
        parser.add_argument('content')
        args = parser.parse_args(strict=True)
        record = usrData(args['datatime'], args['user_id'],
                         args['longitude'], args['latitude'], args['weather'],
                         args['tempe'], args['humi'], args[
                             'pressure'], args['uvIndex'],
                         args['content'])
        try:
            db.session.add(record)
            db.session.commit()
            return {'mesg': '数据上传成功!'}, 200
        except:
            return {'mesg': '数据上传失败!'}, 400


class reltiPerson(Resource):

    """获取geren用户实时信息"""

    def get(self):
        user_id = request.args['user_id']
        record = devData.query.filter_by(user_id=user_id).order_by(
            'datatime desc').limit(1)[0]
        if record is None:
            return {'mesg': '该用户没有上传数据!'}
        result = {}
        result['temperature'] = record.temperature
        result['humidity'] = record.humidity
        result['pressure'] = record.pressure
        result['uvIndex'] = record.uvIndex
        result['datatime'] = record.datatime
        return result, 200


class reltiPeople(Resource):

    def get(self):
        base_time = datetime.datetime.now()
        forwd_time = base_time - datetime.timedelta(hours=2)
        start_time = forwd_time.strftime('%Y-%m-%d %H:%M:%S')
        end_time = base_time.strftime('%Y-%m-%d %H:%M:%S')
        data_list = devData.query.filter(devData.datatime >= start_time,
                                         devData.datatime <= end_time).all()
        if len(data_list) == 0:
            return {'mesg': '没有用户上传数据'}
        user_list = []
        for user in data_list:
            user_list.append(user.user_id)
        user_list = list(set(user_list))
        result = []
        for id in user_list:
            buf = {}
            record = devData.query(user_id=id).order_by(
                'datatime desc').limit(1)[0]
            buf = to_json(record)
            del buf['user_id']
            del buf['device_mac']
            result.append(buf)
        return result, 200
