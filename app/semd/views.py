#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask.ext.restful import Resource
from flask.ext.restful import reqparse
from flask import request
import datetime
import time
from ..models import *
from ..lib.util import *
from ..login.views import auth


class devResource(Resource):
    # decorators = [auth.login_required]

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
        user = User.query.filter_by(id=args['user_id']).first()
        if user is None:
            return {'mesg': '该用户不存在!'}
        datatime = datetime.datetime.strptime(
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
            return {'status': 'fail', 'mesg': '请先绑定设备!'}, 200


class usrResource(Resource):
    # decorators = [auth.login_required]

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


class usrCorrect(Resource):
    # decorators = [auth.login_required]

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('datatime', type=str)
        parser.add_argument('user_id', type=str)
        parser.add_argument('weather')
        parser.add_argument('tempe', type=str)
        parser.add_argument('longitude', type=str)
        parser.add_argument('latitude', type=str)
        parser.add_argument('content')
        args = parser.parse_args(strict=True)
        record = crorrection(args['datatime'], args['user_id'],
                             args['longitude'], args['latitude'],
                             args['weather'], args['tempe'], args['content'])
        try:
            db.session.add(record)
            db.session.commit()
            return {'status': 'success', 'mesg': '数据上传成功!'}, 200
        except:
            return {'status': 'fail', 'mesg': '数据上传失败!'}, 200


class sportResource(Resource):
    # decorators = [auth.login_required]

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
    # decorators = [auth.login_required]
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
        result['uvIndex'] = str(
            round(float(record.uvIndex) / 1000 * 1200 / 365, 1))
        result['datatime'] = record.datatime
        return {'status': 'success', "data": result}


def strTotsp(arg):
    return int(time.mktime(time.strptime(arg, '%Y-%m-%d %H:%M:%S')))


def f4(seq):
    # order preserving
    noDupes = []
    [noDupes.append(i) for i in seq if not noDupes.count(i)]
    return noDupes


class env_history(Resource):
    # decorators = [auth.login_required]

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
        # base_time = datetime.datetime.strptime(
        #     record.datatime, "%Y-%m-%d %H:%M:%S")
        # start_time = base_time - datetime.timedelta(days=1)
        base_time = record.datatime
        start_time = base_time[:11] + "00:00:00"
        # 获取显示总点数, 每隔5分钟一个点
        ponits = (strTotsp(base_time) - strTotsp(start_time)) / 300
        timePts = []
        for i in range(ponits + 1):
            Pt = datetime.datetime.strptime(
                start_time, '%Y-%m-%d %H:%M:%S') + datetime.timedelta(minutes=5 * i)
            timePts.append(Pt.strftime('%Y-%m-%d %H:%M:%S'))
        results = devData.query.filter(
            devData.datatime >= start_time,
            devData.datatime <= record.datatime, devData.user_id == id).all()
        if item == 'tempe':
            tempe_list = []
            timeL = []
            values = []
            # for p in timePts:
            #     t_buf = {}
            #     t_buf['tempe'] = ''
            #     for result in results:
            #         if abs(strTotsp(result.datatime) - strTotsp(p)) < 120:
            #             t_buf['tempe'] = result.temperature
            #     t_buf['time'] = p
            #     tempe_list.append(t_buf)
            for result in results:
                t_buf = {}
                buf_value = ''
                dataTi = result.datatime
                timeUnif = dataTi[:14] + "00:00"
                counts = (strTotsp(dataTi) - strTotsp(timeUnif)) / 300
                formatT = datetime.datetime.strptime(
                    timeUnif, '%Y-%m-%d %H:%M:%S') + datetime.timedelta(minutes=5 * counts)
                if abs(strTotsp(dataTi) - strTotsp(formatT.strftime('%Y-%m-%d %H:%M:%S'))) < 120:
                    buf_value = result.temperature
                    buf_time = formatT.strftime('%Y-%m-%d %H:%M:%S')
                    timeL.append(buf_time)
                    values.append(buf_value)
            noDupes = f4(timeL)
            for i in noDupes:
                t_buf = {}
                t_buf['time'] = i
                t_buf['tempe'] = values[timeL.index(i)]
                tempe_list.append(t_buf)
            return {'status': 'success', "data": tempe_list}
        if item == 'humi':
            humi_list = []
            timeL = []
            values = []
            # for p in timePts:
            #     h_buf = {}
            #     h_buf['humi'] = 0
            #     for result in results:
            #         if abs(strTotsp(result.datatime) - strTotsp(p)) < 120:
            #             h_buf['humi'] = result.humidity
            #     h_buf['time'] = p
            #     humi_list.append(h_buf)
            for result in results:
                t_buf = {}
                buf_value = ''
                dataTi = result.datatime
                timeUnif = dataTi[:14] + "00:00"
                counts = (strTotsp(dataTi) - strTotsp(timeUnif)) / 300
                formatT = datetime.datetime.strptime(
                    timeUnif, '%Y-%m-%d %H:%M:%S') + datetime.timedelta(minutes=5 * counts)
                if abs(strTotsp(dataTi) - strTotsp(formatT.strftime('%Y-%m-%d %H:%M:%S'))) < 120:
                    buf_value = result.humidity
                    buf_time = formatT.strftime('%Y-%m-%d %H:%M:%S')
                    timeL.append(buf_time)
                    values.append(buf_value)
            noDupes = f4(timeL)
            for i in noDupes:
                t_buf = {}
                t_buf['time'] = i
                t_buf['humi'] = values[timeL.index(i)]
                humi_list.append(t_buf)
            return {'status': 'success', "data": humi_list}
        if item == 'uv':
            uv_list = []
            timeL = []
            values = []
            # for p in timePts:
            #     u_buf = {}
            #     u_buf['uv'] = 0
            #     for result in results:
            #         if abs(strTotsp(result.datatime) - strTotsp(p)) < 120:
            #             u_buf['uv'] = result.uvIndex
            #     u_buf['time'] = p
            #     uv_list.append(u_buf)
            for result in results:
                t_buf = {}
                buf_value = ''
                dataTi = result.datatime
                timeUnif = dataTi[:14] + "00:00"
                counts = (strTotsp(dataTi) - strTotsp(timeUnif)) / 600
                formatT = datetime.datetime.strptime(
                    timeUnif, '%Y-%m-%d %H:%M:%S') + datetime.timedelta(minutes=10 * counts)
                if abs(strTotsp(dataTi) - strTotsp(formatT.strftime('%Y-%m-%d %H:%M:%S'))) < 120:
                    buf_value = result.uvIndex
                    buf_time = formatT.strftime('%Y-%m-%d %H:%M:%S')
                    timeL.append(buf_time)
                    values.append(buf_value)
            noDupes = f4(timeL)
            for i in noDupes:
                t_buf = {}
                t_buf['time'] = i
                t_buf['uv'] = values[timeL.index(i)]
                uv_list.append(t_buf)
            return {'status': 'success', "data": uv_list}
