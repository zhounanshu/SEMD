#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pymongo import MongoClient
import urllib2
import json
import datetime
from config import *
# acquire data via Restful, weather forecast , frequecny:1 day
header = {"Accept": " application/json",
          "Content-Type": " application/json"}
req = urllib2.Request(forecast_10, headers=header)
response = urllib2.urlopen(req).read()
results = {}
results['data'] = json.loads(response)
results['msg'] = '10天天气预报'
results['acquire_time'] =  datetime.datetime.now().strftime('%y-%m-%d %H:%M')


# store weather forecast data to mongoDB
client = MongoClient('localhost', 27017)
db = client['meteorShanghai']
collection = db['forecastTen']
post_id = collection.insert_one(results).inserted_id

