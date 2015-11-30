#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask.ext.restful import Resource
from flask.ext.restful import reqparse
from flask import request
import datetime
import time
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
        print start_time
        print end_time
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
            record = devData.query.filter_by(user_id=id).order_by(
                'datatime desc').limit(1)[0]
            buf = to_json(record)
            del buf['user_id']
            del buf['device_mac']
            result.append(buf)
        return result, 200


class env_history(Resource):

    def get(self):
        id = request.args['user_id']
        item = request.args['item']
        items = set(['tempe', 'humi', 'uv'])
        if item not in items:
            return {'mesg': 'url参数错误!'}, 200
        record = devData.query.filter_by(
            user_id=id).order_by('datatime desc').first()
        if record is None:
            return {'mesg': '你还未使用设备!'}, 200
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
            return tempe_list, 200
        if item == 'humi':
            humi_list = []
            for result in results:
                h_buf = {}
                h_buf['time'] = result.datatime
                h_buf['humi'] = result.humidity
                humi_list.append(h_buf)
            return humi_list, 200
        if item == 'uv':
            uv_list = []
            for result in results:
                u_buf = {}
                u_buf['time'] = result.datatime
                u_buf['uv'] = result.uvIndex
                uv_list.append(u_buf)
            return uv_list, 200
