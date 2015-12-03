#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import request
import datetime
from flask.ext.restful import Resource
import urllib2
import json
from .config import *
from ..models import *
from ..lib.util import *


class viewRelti(Resource):

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

    def post(self):
        pass

    def put(self):
        pass

    def delete(self):
        pass


class viewForecast(Resource):

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

    def get(self):
        area = request.args['area']
        records = cityAlarm.query.filter(
            cityAlarm.publishtime == datetime.datetime.now().strftime(
                '%Y-%m-%d'), area=area)
        if records.id is None:
            return {'status': 'fail', "mesg": "数据缺失"}
        data = []
        for record in records:
            temp = {}
            temp = to_json_list(record)
            data.append(temp)
        return {'status': 'success', "data": data}

        def post(self):
            pass

        def put(self):
            pass

        def delete(self):
            pass


class get_alarm(Resource):

    def get(self):
        response = urllib2.urlopen(url).read()
        response = json.loads(response)
        return {'status': 'success', "data": response}


class get_realtime(Resource):

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
        aqi_req = urllib2.Request(aqi_url, headers=header)
        aqi_response = urllib2.urlopen(aqi_req).read()
        aqi = json.loads(aqi_response)['aqi']
        if aqi is None:
            return {'status': "fail", 'mesg': "aqi数据缺失!"}
        temp['aqi'] = aqi
        return {'status': 'success', "data": temp}


class get_forecast(Resource):

    def get(self):
        area = request.args['area']
        header = {"Accept": " application/json",
                  "Content-Type": " application/json"}
        req = urllib2.Request(forecast_url, headers=header)
        response = urllib2.urlopen(req).read()
        response = json.loads(response)
        return {'status': 'success', "data": response}


class get_rain(Resource):

    def get(self):
        lon = request.args['lon']
        lat = request.args['lat']
        rain_url = rain_pre + '&lon=' + str(lon) + '&lat=' + str(lat)
        header = {"Accept": " application/json",
                  "Content-Type": " application/json"}
        req = urllib2.Request(rain_url, headers=header)
        response = urllib2.urlopen(req).read()
        response = json.loads(response)['data']
        return {'status': 'success', "data": response}
