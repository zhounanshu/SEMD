#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask.ext.restful import Resource
import datetime
import math
from decimal import *
from ..models import *
from ..lib.util import *


def rad(arg):
    return float(arg) ** math.pi / 180


def distance(lat1, lng1, lat2, lng2):
    radlat1 = rad(lat1)
    radlat2 = rad(lat2)
    a = radlat1 - radlat2
    b = rad(lng1) - rad(lng2)
    s = 2 * math.asin(math.sqrt(math.pow(math.sin(a / 2), 2) +
                                math.cos(radlat1) * math.cos(radlat2) * math.pow(math.sin(b / 2), 2)))
    earth_radius = 6378.137 * 1000
    s = s * earth_radius
    if s < 0:
        return -s
    else:
        return s


class reltiPeople(Resource):

    def get(self):
        base_time = datetime.datetime.now()
        forwd_time = base_time - datetime.timedelta(hours=2)
        start_time = forwd_time.strftime('%Y-%m-%d %H:%M:%S')
        end_time = base_time.strftime('%Y-%m-%d %H:%M:%S')
        data_list = devData.query.filter(devData.datatime >= start_time,
                                         devData.datatime <= end_time).all()
        if len(data_list) == 0:
            return {'status': 'fail', 'mesg': '没有用户上传数据'}
        user_list = []
        for user in data_list:
            user_list.append(user.user_id)
        user_list = list(set(user_list))
        result = []
        for id in user_list:
            buf = {}
            record = devData.query.filter_by(user_id=id).order_by(
                devData.datatime.desc()).limit(1)[0]
            buf = to_json(record)
            # del buf['user_id']
            del buf['device_mac']
            result.append(buf)
        device_real = []
        for user in result:
            post_num = 0
            for value in result:
                if distance(user['latitude'], user['longitude'],
                            value['latitude'], value['longitude']) <= 1000:
                    post_num += 1
            user['post_num'] = post_num
            del user['id']
            device_real.append(user)
        return {'status': 'success', "data": device_real}
