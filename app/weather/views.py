#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import request, send_file
import datetime
from flask.ext.restful import Resource
from flask.ext.restful import reqparse
import urllib2
import sys
import os
import re
import json
from .config import *
from ..models import *
from ..lib.util import *
from ..login.views import auth
sys.path.append('..')


type_codes = ['a', 'b', 'c', 'd', 'e', 'f',
              'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o']
alarm_types = ['台风', '暴雨', '暴雪', '寒潮', '大风', '大雾', '雷电',
               '冰雹', '霜冻', '高温', '干旱', '道路结冰', '霾', '沙城暴', '臭氧']
alarm_levels = ['蓝色', '黄色', '橙色', '红色', '解除']
types = dict(zip(alarm_types, type_codes))


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


class realWether(Resource):
    # decorators = [auth.login_required]

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('datetime', type=str)
        parser.add_argument('name', type=str)
        parser.add_argument('sitenumber', type=str)
        parser.add_argument('tempe', type=str)
        parser.add_argument('rain', type=str)
        parser.add_argument('wind_direction')
        parser.add_argument('wind_speed')
        parser.add_argument('visibility', type=str)
        parser.add_argument('humi', type=str)
        parser.add_argument('pressure', type=str)
        args = parser.parse_args(strict=True)
        record = reltiWeather(args['datetime'], args['name'],
                              args['sitenumber'], args['tempe'],
                              args['humi'], args['wind_direction'],
                              args['wind_speed'], args['pressure'],
                              args['rain'], args['visibility'])
        db.session.add(record)
        try:
            db.session.commit()
        except:
            return {'mesg': "添加数据失败"}, 200
        return {'mesg': "添加数据成功!"}, 200


class realAqi(Resource):
    # decorators = [auth.login_required]

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('datetime', type=str)
        parser.add_argument('aqi', type=str)
        parser.add_argument('level')
        parser.add_argument('pripoll')
        parser.add_argument('content')
        parser.add_argument('measure')
        args = parser.parse_args(strict=True)
        record = reltiAqi(args['datetime'], args['aqi'], args['level'], args[
                          'pripoll'], args['content'], args['measure'])
        db.session.add(record)
        try:
            db.session.commit()
        except:
            return {"mesg": "添加数据失败!"}, 200
        return {'mesg': "添加数据成功!"}, 200


class foreWeat(Resource):
    # decorators = [auth.login_required]

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('datetime', type=str)
        parser.add_argument('view_time', type=str)
        parser.add_argument('direction', type=str)
        parser.add_argument('speed', type=str)
        parser.add_argument('tempe', type=str)
        parser.add_argument('weather', type=str)
        parser.add_argument('weatherpic', type=str)
        parser.add_argument('area', type=str)
        record = foreWeather(args['datetime'], args['view_time'],
                             args['direction'], args['speed'],
                             args['tempe'], args['weather'],
                             args['weatherpic'])
        db.session.add(record)
        try:
            db.session.commit()
        except:
            return {'mesg': '数据添加失败!'}, 200
        return {'mesg': '数据添加成功!'}, 200


class wea_Station(Resource):
    # decorators = [auth.login_required]

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('datetime', type=str)
        parser.add_argument('site_name', type=str)
        parser.add_argument('tempe', type=str)
        parser.add_argument('rain', type=str)
        parser.add_argument('humi', type=str)
        parser.add_argument('air_press', type=str)
        parser.add_argument('wind_direction', type=str)
        parser.add_argument('wind_speed', type=str)
        parser.add_argument('vis', type=str)
        parser.add_argument('lon', type=str)
        parser.add_argument('lat', type=str)
        record = weaStation(args['datetime'], args['site_name'], args['tempe'],
                            args['rain'], args['humi'], args['air_press'],
                            args['wind_direction'], args['wind_speed'],
                            args['vis'], args['lon'], args['lat'])
        db.session.add(record)
        try:
            db.session.commit()
        except:
            return {'mesg': '数据添加失败!'}
        return {'mesg': "数据添加成功!"}


class viewRelti(Resource):
    # decorators = [auth.login_required]

    def get(self):
        area = request.args['area']
        time = request.args['time']
        record = reltiWeather.query.filter_by(
            reltiWeather.name == area
        ).order_by('datetime desc').limit(1)
        if record.id is None:
            return {'status': 'fail', "mesg": "数据缺失!"}
        aqi_record = reltiAqi.query().order_by('datetime desc').limit(1)
        data = {}
        data['tempe'] = record[0].tempe
        data['humi'] = record[0].humi
        data['pressure'] = record[0].pressure
        data['wind_direction'] = record[0].wind_direction
        data['wind_speed'] = record[0].wind_speed
        data['aqi'] = aqi_record[0].aqi
        data['level'] = aqi_record[0].level
        return {'status': 'success', "data": data}, 200


class viewForecast(Resource):
    # decorators = [auth.login_required]

    def get(self):
        area = request.args['area']
        time = request.args['time']
        records = foreWeather.query.filter(
            foreWeather.view_time == datetime.datetime.now().strftime(
                '%Y-%m-%d'), area=area)
        if records.id is None:
            return {'status': 'fail', "mesg": "数据缺失"}
        data = []
        for record in records:
            temp = {}
            temp = to_json_list(record)
            del tempe['view_time']
            data.append(temp)
        return {'status': 'success', "data": data}

    def post(self):
        pass

    def put(self):
        pass

    def delete(self):
        pass


class alarm(Resource):
    # decorators = [auth.login_required]

    def get(self):
        record = cityAlarm.query.order_by(cityAlarm.publishtime.desc()).all()
        if record is None:
            return {'status': 'fail', "mesg": "数据缺失"}
        data = to_json_list(record)
        result = []
        for elem in data:
            if elem['level'] != "解除".decode('utf-8'):
                if elem['level'] is not None:
                    level_code = alarm_levels.index(
                        elem['level'].encode('utf-8'))
                    type_code = types[elem['type'].encode('utf-8')]
                    img_name = type_code + str(level_code)
                    elem['img_name'] = img_name
                    del elem['id']
                else:
                    return {'mesg': '数据缺失!'}
            else:
                elem['img_name'] = None
                del elem['id']
                result.append(elem)
        return {'status': 'success', "data": data}

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('publishtime', type=str)
        parser.add_argument('type')
        parser.add_argument('level')
        parser.add_argument('content')
        args = parser.parse_args(strict=True)
        record = cityAlarm(args['publishtime'], args['type'],
                           args['level'], args['content'])
        db.session.add(record)
        try:
            db.session.commit()
        except:
            return {'mesg': "上传数据失败!"}
        return {'mesg': '上传数据成功!'}

    def put(self):
        pass

    def delete(self):
        pass


class get_alarm(Resource):
    # decorators = [auth.login_required]

    def get(self):
        response = urllib2.urlopen(url).read()
        response = json.loads(response)
        result = []
        for elem in response:
            if elem['level'] != "解除".decode('utf-8'):
                level_code = alarm_levels.index(elem['level'].encdoe('utf-8'))
                type_code = types[elem['type'].encode('utf-8')]
                img_name = type_code + str(level_code)
                elem['img_name'] = img_name
            else:
                elem['img_name'] = None
                result.append(elem)
        return {'status': 'success', "data": result}


class alarm_img(Resource):
    # decorators = [auth.login_required]

    def get(self):
        img_name = request.args['img_name']
        path = os.path.split(os.path.realpath(__file__))[0] + '/alarm_pic'
        img = os.path.join(path, img_name + '.jpg')
        return send_file(img)


class get_realtime(Resource):
    # decorators = [auth.login_required]

    def get(self):
        area = request.args['area']
        header = {"Accept": " application/json",
                  "Content-Type": " application/json"}
        req = urllib2.Request(weather_url, headers=header)
        response = urllib2.urlopen(req).read()
        result = json.loads(response)['data']
        temp = {}
        for dic in result:
            if dic['name'] == area:
                temp = dic
        if temp is None:
            return {'status': "fail", 'mesg': '该区域数据缺失!'}
        invalid_keys = ['sitenumber', 'rain', 'visibility']
        for key in invalid_keys:
            del temp[key]
        if not isData(temp['wind_speed']):
            temp['wind_speed'] = 0
        if not isData(temp['wind_direction']):
            temp['wind_direction'] = 0
        temp['wind_speed'] = str(wind_speed(temp['wind_speed'])) + '级'
        temp['wind_direction'] = wind_direct(
            temp['wind_direction']) + '风'
        aqi_req = urllib2.Request(aqi_url, headers=header)
        aqi_response = urllib2.urlopen(aqi_req).read()
        aqi = json.loads(aqi_response)['aqi']
        if aqi is None:
            return {'status': "fail", 'mesg': "aqi数据缺失!"}
        temp['aqi'] = aqi
        return {'status': 'success', "data": temp}

weather_pic = ['晴', '多云', '阴', '小雨', '小雪', '阵雨', '中雨', '中雪', '雷阵雨',
               '雨夹雪', '大雨', '大雪', '暴雨', '暴雪', '大暴雨', '特大暴雨', '冰雹',
               '沙尘暴', '雾', '浮尘', '扬尘', '扬沙', '强沙尘暴']
weather_spe = ['雨', '雪', '霾']
haze_degree = ['轻', '中', '重']


def get_weather_pic(pic_str, keys):
    buf = []
    for f in keys:
        if pic_str.find(f.decode('utf8')) != -1:
            buf.append(f)
    return buf


def get_spec_weather(pic_str, reg):
    special = None
    pattern = re.compile(reg)
    special = re.findall(pattern, pic_str)
    return special


def find_weather(pre_pic, post_pic, reg, flag):
    temp = []
    if len(get_spec_weather(pre_pic, reg)) > 0:
        temp.append(flag)
    else:
        weather_buf = get_weather_pic(pre_pic, weather_pic)
        if len(weather_buf) != 0:
            temp.append(weather_buf[-1])
    if len(get_spec_weather(post_pic, reg)) > 0:
        temp.append(flag)
    else:
        weather_buf = get_weather_pic(post_pic, weather_pic)
        if len(weather_buf) != 0:
            temp.append(weather_buf[-1])
    return temp


class get_forecast(Resource):
    # decorators = [auth.login_required]

    def get(self):
        area = request.args['area']
        header = {"Accept": " application/json",
                  "Content-Type": " application/json"}
        req = urllib2.Request(forecast_url, headers=header)
        response = urllib2.urlopen(req).read()
        response = json.loads(response)
        result = []
        for n in response:
            temp = []
            weather_state = n['weatherpic']
            if weather_state.find('有'.decode('utf8')) == -1:
                weather_buf = get_weather_pic(weather_state, weather_pic)
                if len(weather_buf) != 0:
                    if len(weather_buf) == 1:
                        temp = [weather_buf[0]] * 2
                    else:
                        temp.append(weather_buf[0])
                        temp.append(weather_buf[-1])
                else:
                    temp = ['晴', '多云']
            else:
                if weather_state.find('转'.decode('utf8')) != -1:
                    buf = weather_state.split('转'.decode('utf8'))
                    rain_buf = find_weather(buf[0], buf[-1], r'雨', '小雨')
                    if len(rain_buf) >= 2:
                        temp.append(rain_buf[0])
                        temp.append(rain_buf[-1])
                    else:
                        snow_buf = find_weather(buf[0], buf[-1], r'雪', '小雪')
                        if len(snow_buf) >= 2:
                            temp.append(snow_buf[0])
                            temp.append(snow_buf[-1])
                        else:
                            if get_spec_weather(weather_state,
                                                r'重') is not None:
                                temp = ['阴', '重度雾霾']
                            elif get_spec_weather(weather_state,
                                                  r'中') is not None:
                                temp = ['阴', '中度雾霾']
                            elif get_spec_weather(weather_state,
                                                  r'轻') is not None:
                                temp = ['阴', '轻度雾霾']
                            else:
                                temp = ['阴', '多云']
                else:
                    if get_spec_weather(weather_state, r'雨') is not None:
                        temp = ['小雨', '小雨']
                    elif get_spec_weather(weather_state, r'雪') is not None:
                        temp = ['小雪', '小雪']
                    elif get_spec_weather(weather_state, r'霾') is not None:
                        if get_spec_weather(weather_state, r'重') is not None:
                            temp = ['阴', '重度雾霾']
                        elif get_spec_weather(weather_state, r'中') is not None:
                            temp = ['阴', '中度雾霾']
                        else:
                            temp = ['阴', '轻度雾霾']
                    else:
                        temp = ['多云', '阴']
            n['weatherpic'] = temp
            # n['tempe_l'] = n['tempe'].split('~')[0]
            # n['tempe_h'] = n['tempe'].split('~')[1][:-1]
            result.append(n)
        for i in range(len(result)):
            for key in result[i].keys():
                if key == 'tempe':
                    if result[i][key].split('~')[0] == '':
                        result[i][key] = result[
                            i - 1][key] if i > 0 else result[i + 1][key]
                if result[i][key] == None:
                    result[i][key] = result[
                        i - 1][key] if i > 0 else result[i + 1][key]
                    result[i]['weather'] = '晴'
        return {'status': 'success', "data": response}


class get_rain(Resource):
    # decorators = [auth.login_required]

    def get(self):
        lon = request.args['lon']
        lat = request.args['lat']
        rain_url = rain_pre + '&lon=' + str(lon) + '&lat=' + str(lat)
        header = {"Accept": " application/json",
                  "Content-Type": " application/json"}
        req = urllib2.Request(rain_url, headers=header)
        response = urllib2.urlopen(req).read()
        response = json.loads(response)['data']['list']
        rain_list = []
        for elem in response:
            rain_list.append(elem['d'])
        if float(rain_list[0]) == 0:
            count = 0
            for i in range(len(rain_list)):
                if float(rain_list[i]) != 0:
                    count = i
                    break
            if count != 0:
                mesg = '当前位置没有雨,' + str(count * 6) + '分钟后降雨'
                return {'status': 'success', 'mesg': mesg}
            else:
                mesg = '当前位置没有雨，未来90分钟不会下雨'
                return {'status': 'success', 'mesg': mesg}
        else:
            count = 0
            for i in range(len(rain_list) - 1):
                if rain_list[i] < rain_list[i + 1]:
                    count += 1
            if count == 15:
                return {'status': 'success', 'mesg': '当前位置有雨, 未来90分钟累计降雨量为' +
                        str(rain_list[15]) + 'mm'}
            else:
                count = 0
                flag = False
                for i in range(len(rain_list) - 1):
                    for j in range(len(rain_list) - 1 - i):
                        if rain_list[i] == rain_list[j + i + 1]:
                            count = i
                            flag = True
                            break
                    if flag:
                        break
                mesg = '当前位置有雨, 未来' + \
                    str(count * 6) + '分钟降雨量为' + \
                    str(rain_list[count]) + 'mm, 之后雨停'
                return{'status': 'success', 'mesg': mesg}


from math import *


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


class get_qpf(Resource):
    # decorators = [auth.login_required]

    def get(self):
        header = {'Accept': 'application/json',
                  'Content-Type': 'application/json'}
        request = urllib2.Request(rain_qpf, headers=header)
        response = urllib2.urlopen(request).read()
        records = json.loads(response)['data']
        '''
                        雨量预测测试
        '''
        for value in records:
            if distance('31.87', '121.33', value['lat'], value['lon']) < 100000:
                value['data'] = str(random.random())[:3]
        result = []
        for value in records:
            if value['data'] != 0:
                result.append(value)
        return {'status': 'success', 'data': result}


class autoStation(Resource):
    # decorators = [auth.login_required]

    def get(self):
        header = {"Accept": " application/json",
                  "Content-Type": " application/json"}
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
                    buf['tempe'] = record['tempe']
                    buf['rain'] = record['rain']
                    buf['location'] = location.site_name
                    buf['wind_direction'] = wind_direct(
                        record['wind_direction']) + '风'
                    buf['wind_speed'] = str(
                        wind_speed(record['wind_speed'])) + '级'
                    buf['datetime'] = record['datetime']
                    result.append(buf)
        if result is None:
            return {'status': 'fail', 'mesg': '缺失数据!'}
        return {'mesg': '自动站信息', 'status': 'success', 'data': result}


class weatherLocation(Resource):
    # decorators = [auth.login_required]

    def get(self):
        jd = request.args['jd']
        wd = request.args['wd']
        header = {"Accept": " application/json",
                  "Content-Type": " application/json"}
        url = loca_url + "jd=" + jd + '&' + "wd=" + wd
        req = urllib2.Request(url, headers=header)
        response = urllib2.urlopen(req).read()
        result = json.loads(response)
        temp = {}
        pattern_d = re.compile('\d{4}-\d{2}-\d{2}.*?')
        pattern_h = re.compile('\d{2}:\d{2}:\d{2}.*?')
        s = result['datetime']
        d_temp = re.findall(pattern_d, s)
        h_temp = re.findall(pattern_h, s)
        if len(d_temp) > 0 and len(h_temp) > 0:
            time = d_temp[0] + ' ' + h_temp[0]
        else:
            time = ''
        temp['datetime'] = time
        temp['pressure'] = result['pressure']
        temp['tempe'] = result['tempe']
        temp['humi'] = result['humi']
        temp['wind_direction'] = result['wind_direction']
        temp['wind_speed'] = result['wind_speed']
        if not isData(temp['wind_speed']):
            temp['wind_speed'] = 0
        if not isData(temp['wind_direction']):
            temp['wind_direction'] = 0
        temp['wind_speed'] = str(wind_speed(temp['wind_speed'])) + '级'
        temp['wind_direction'] = wind_direct(
            temp['wind_direction']) + '风'
        aqi_req = urllib2.Request(aqi_url, headers=header)
        aqi_response = urllib2.urlopen(aqi_req).read()
        aqi = json.loads(aqi_response)['aqi']
        if aqi is None:
            return {'status': "fail", 'mesg': "aqi数据缺失!"}
        temp['aqi'] = aqi
        return {'status': 'success', "data": temp}


class get_disAla(Resource):
    # decorators = [auth.login_required]
    def get(self):
        area = request.args['area']
        header = {"Accept": " application/json",
                  "Content-Type": " application/json",
                  "User-Agent": "Mozilla/5.1"}
        url = district_url + area.encode('utf8')
        req = urllib2.Request(url, headers=header)
        response = urllib2.urlopen(req).read()
        response = json.loads(response)
        result = []
        for elem in response['data']:
            if elem['level'] != "解除".decode('utf8'):
                level_code = alarm_levels.index(elem['level'].encode('utf-8'))
                type_code = types[elem['type'].encode('utf8')]
                img_name = type_code + str(level_code)
                elem['img_name'] = img_name
            else:
                elem['img_name'] = None
            result.append(elem)
        return {'status': 'success', "data": result, 'mesg': response['msg']}


class hasAlarm(Resource):
    def get(self):
        areas = ['青浦', '松江', '金山', '闵行', '市区', '宝山', '嘉定', '浦东', '奉贤', '崇明']
        header = {"Accept": " application/json",
                  "Content-Type": " application/json"}
        result = []
        for area in areas:
            url = district_url + area
            req = urllib2.Request(url, headers=header)
            response = urllib2.urlopen(req).read()
            response = json.loads(response)['data']
            if len(response) != 0:
                for ele in response:
                    if ele['level'] != u'解除':
                        result.append(area)
                        break
        return {'status': 'success', 'areas': result}, 200


class threeHour(Resource):
    def get(self):
        header = {"Accept": " application/json",
                  "Content-Type": " application/json"}
        req = urllib2.Request(three_hour, headers=header)
        response = urllib2.urlopen(req).read()
        response = json.loads(response)['data']['content']
        result = response.split('\r\n')[2]
        temp = re.findall(r"本市：(.*?)，", result.encode('utf8'))
        print temp
        weather = ''
        if len(temp) != 0:
            weather = temp[0]
        return {'status': 'success', 'data': weather}, 200
