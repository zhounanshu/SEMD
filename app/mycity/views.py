#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask.ext.restful import Resource
import datetime
from math import *
import urllib2
import json
from decimal import *
from ..weather.config import *
from ..models import *
from ..lib.util import *
from ..login.views import auth

def isValid(data):
    flag = 0
    for key in data.keys():
        if data[key] == 99999:
            flag += 1
    if flag == 0:
        return True
    return False


def isData(data):
    if data == 99999:
        return False
    else:
        return True


def DataCheck(data):
    if data != '':
        return True
    return False


def wind_direct(wind_direction):
    wind_direct = None
    if 22.6 <= float(wind_direction) and float(wind_direction) <= 67.5:
        wind_direct = '东北'
    if 67.6 <= float(wind_direction) and float(wind_direction) <= 112.5:
        wind_direct = '东'
    if 112.6 <= float(wind_direction) and float(wind_direction) <= 157.5:
        wind_direct = '东南'
    if 157.6 <= float(wind_direction) and float(wind_direction) <= 202.5:
        wind_direct = '南'
    if 202.6 <= float(wind_direction) and float(wind_direction) <= 247.5:
        wind_direct = '西南'
    if 247.6 <= float(wind_direction) and float(wind_direction) <= 292.5:
        wind_direct = '西'
    if 292.6 <= float(wind_direction) and float(wind_direction) <= 337.5:
        wind_direct = '西北'
    if 337.6 <= float(wind_direction) or float(wind_direction) <= 22.5:
        wind_direct = '北'
    return wind_direct


def wind_speed(wind_speed):
    wind_order = None
    if 0 <= float(wind_speed) <= 0.2:
        wind_order = 0
    if 0.3 <= float(wind_speed) <= 1.5:
        wind_order = 1
    if 1.6 <= float(wind_speed) <= 3.3:
        wind_order = 2
    if 3.4 <= float(wind_speed) <= 5.4:
        wind_order = 3
    if 5.5 <= float(wind_speed) <= 7.9:
        wind_order = 4
    if 8.0 <= float(wind_speed) <= 10.7:
        wind_order = 5
    if 10.8 <= float(wind_speed) <= 13.8:
        wind_order = 6
    if 13.9 <= float(wind_speed) <= 17.1:
        wind_order = 7
    if 17.2 <= float(wind_speed) <= 20.7:
        wind_order = 8
    if 20.8 <= float(wind_speed) <= 24.4:
        wind_order = 9
    if 24.5 <= float(wind_speed) <= 28.4:
        wind_order = 10
    if 28.5 <= float(wind_speed) <= 32.6:
        wind_order = 11
    return wind_order


def distance(Lat_A, Lng_A, Lat_B, Lng_B):

    ra = 6378.140  # 赤道半径 (km)
    rb = 6356.755  # 极半径 (km)
    flatten = (ra - rb) / ra  # 地球扁率
    if (Lat_A == Lat_B) and (Lng_A == Lng_B):
        return 0
    rad_lat_A = radians(Lat_A)
    rad_lng_A = radians(Lng_A)
    rad_lat_B = radians(Lat_B)
    rad_lng_B = radians(Lng_B)
    pA = atan(rb / ra * tan(rad_lat_A))
    pB = atan(rb / ra * tan(rad_lat_B))
    xx = acos(sin(pA) * sin(pB) + cos(pA) * cos(pB)
              * cos(rad_lng_A - rad_lng_B))
    c1 = (sin(xx) - xx) * (sin(pA) + sin(pB)) ** 2 / cos(xx / 2) ** 2
    c2 = (sin(xx) + xx) * (sin(pA) - sin(pB)) ** 2 / sin(xx / 2) ** 2
    dr = flatten / 8 * (c1 - c2)
    distance = ra * (xx + dr)
    return distance * 1000


class reltiPeople(Resource):
    # decorators = [auth.login_required]

    def get(self):
        header = {"Accept": " application/json",
                  "Content-Type": " application/json",
                  "User-Agent": "Mozilla/5.1"}
        req = urllib2.Request(station_url, headers=header)
        response = urllib2.urlopen(req).read()
        response = json.loads(response)['data']
        result = []
        for record in response:
            buf = {}
            location = site_infor.query.filter_by(
                site_name=record['site_name']).first()
            if location is not None:
                if wind_direct(record['wind_direction']) is not None and wind_speed(record['wind_speed']) is not None:
                    buf['longitude'] = location.longitude
                    buf['latitude'] = location.latitude
                    buf['location'] = location.site_name
                    buf['tempe'] = record['tempe']
                    buf['rain'] = record['rain']
                    buf['wind_direction'] = wind_direct(
                        record['wind_direction']) + '风'
                    buf['wind_speed'] = str(
                        wind_speed(record['wind_speed'])) + '级'
                    buf['datetime'] = record['datetime']
                    result.append(buf)
        if result is None:
            return {'status': 'fail', 'mesg': '自动站缺失数据!'}
        base_time = datetime.datetime.now()
        forwd_time = base_time - datetime.timedelta(hours=2)
        start_time = forwd_time.strftime('%Y-%m-%d %H:%M:%S')
        end_time = base_time.strftime('%Y-%m-%d %H:%M:%S')
        data_list = devData.query.filter(devData.datatime >= start_time,
                                         devData.datatime <= end_time).all()
        device_real = []
        if len(data_list) != 0:
            user_list = []
            for user in data_list:
                user_list.append(user.user_id)
            user_list = list(set(user_list))
            result1 = []
            for id in user_list:
                buf = {}
                rd = devData.query.filter_by(user_id=id).order_by(
                    devData.datatime.desc()).limit(1)[0]
                buf = to_json(rd)
                del buf['device_mac']
                result1.append(buf)
            for user in result1:
                post_num = 0
                for value in result1:
                    try:
                        if distance(float(user['latitude']),
                                    float(user['longitude']), float(value['latitude']),
                                    float(value['longitude'])) <= 1000:
                            post_num += 1
                    except:
                        continue
                if user['latitude'] == '' or user['longitude'] == '':
                    continue
                user['post_num'] = post_num
                del user['id']
                count = 0
                for key in user.keys():
                    if DataCheck(user[key]):
                        count += 1
                if count != 9:
                    continue
                device_real.append(user)
        dev_data = {}
        dev_data['source'] = '1'
        dev_data['resource'] = device_real
        station_data = {}
        station_data['source'] = '2'
        station_data['resource'] = result
        container = []
        container.append(dev_data)
        container.append(station_data)
        return {'status': 'success', "data": container}
