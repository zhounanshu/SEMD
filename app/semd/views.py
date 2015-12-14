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
        datatime = datetime.strptime(
            args['datatime'], '%Y-%m-%d %H:%M:%S')
        record = devData(datatime, args['device_mac'],
                         args['user_id'], args['longitude'], args['latitude'],
                         args['temperature'], args['humidity'],
                         args['pressure'], args['uvIndex'])
        try:
            db.session.add(record)
            db.session.commit()
            return {'status': 'success', 'mesg': '数据上传成功!'}, 200
        except:
            return {'status': 'fail', 'mesg': '数据上传失败!'}, 200


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
            return {'status': 'success', 'mesg': '数据上传成功!'}, 200
        except:
            return {'status': 'fail', 'mesg': '数据上传失败!'}, 200


class sportResource(Resource):

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
        parser.add_argument('distance', type=str)
        args = parser.parse_args(strict=True)
        record = sport(args['datatime'], args['device_mac'],
                       args['user_id'], args['longitude'], args['latitude'],
                       args['temperature'], args['humidity'],
                       args['pressure'], args['uvIndex'], args['distance'])
        try:
            db.session.add(record)
            db.session.commit()
            return {'status': 'success', 'mesg': '数据上传成功!'}, 200
        except:
            return {'status': 'fail', 'mesg': '数据上传失败!'}, 200


class reltiPerson(Resource):

    """获取geren用户实时信息"""

    def get(self):
        user_id = request.args['user_id']
        record = devData.query.filter_by(user_id=user_id).order_by(
            'datatime desc').limit(1)[0]
        if record is None:
            return {'status': 'fail', 'mesg': '该用户没有上传数据!'}
        result = {}
        result['temperature'] = record.temperature
        result['humidity'] = record.humidity
        result['pressure'] = record.pressure
        result['uvIndex'] = record.uvIndex
        result['datatime'] = record.datatime
        return {'status': 'success', "data": result}


class env_history(Resource):

    def get(self):
        id = request.args['user_id']
        item = request.args['item']
        items = set(['tempe', 'humi', 'uv'])
        if item not in items:
            return {'status': 'fail', 'mesg': 'url参数错误!'}, 200
        record = devData.query.filter_by(
            user_id=id).order_by('datatime desc').first()
        if record is None:
            return {'status': 'fail', 'mesg': '你还未使用设备!'}, 200
        base_time = datetime.datetime.strptime(
            record.datatime, "%Y-%m-%d %H:%M:%S")
        start_time = base_time - datetime.timedelta(days=1)
        results = devData.query.filter(
            devData.datatime >= start_time.strftime('%Y-%m-%d %H:%M:%S'),
            devData.datatime <= record.datatime).all()
        if item == 'tempe':
            tempe_list = []
            for result in results:
                t_buf = {}
                t_buf['time'] = result.datatime
                t_buf['tempe'] = result.temperature
                tempe_list.append(t_buf)
            return {'status': 'success', "data": tempe_list}
        if item == 'humi':
            humi_list = []
            for result in results:
                h_buf = {}
                h_buf['time'] = result.datatime
                h_buf['humi'] = result.humidity
                humi_list.append(h_buf)
            return {'status': 'success', "data": humi_list}
        if item == 'uv':
            uv_list = []
            for result in results:
                u_buf = {}
                u_buf['time'] = result.datatime
                u_buf['uv'] = result.uvIndex
                uv_list.append(u_buf)
            return {'status': 'success', "data": uv_list}
