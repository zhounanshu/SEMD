#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pymongo import MongoClient
import urllib2
import json
import datetime
from config import *
import cPickle
# acquire data via Restful, frequency: 1 hour
acquire_time = datetime.datetime.now().strftime('%y-%m-%d %H:%M')
client = MongoClient('localhost', 27017)
db = client['meteorShanghai']
header = {"Accept": " application/json",
          "Content-Type": " application/json"}


# store weather forecast data to mongoDB
req = urllib2.Request(air_condition, headers=header)
response = urllib2.urlopen(req).read()
results = json.loads(response)
results['acquire_time'] = acquire_time
collection = db['aircondition']
post_id = collection.insert_one(results).inserted_id

# store shor forecaste weather data
req = urllib2.Request(short_forecast , headers=header)
response = urllib2.urlopen(req).read()
results = json.loads(response)
results['acquire_time'] = acquire_time
collection = client['shortForecast']
post_id = collection.insert_one(results).inserted_id
