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
header = {"Accept": " application/json",
          "Content-Type": " application/json"}
req = urllib2.Request(station_real, headers=header)
response = urllib2.urlopen(req).read()
results = json.loads(response)
results['acquire_time'] = acquire_time

# connect to mongoDB
client = MongoClient('localhost', 27017)
db = client['meteorShanghai']

# insert 80autostaion data
collection = db['autoStation']
post_id = collection.insert_one(results).inserted_id

# insert another station
req = urllib2.Request(station , headers=header)
response = urllib2.urlopen(req).read()
results = json.loads(response)
results['acquire_time'] = acquire_time
collection = db['anotherStation']
post_id = collection.insert_one(results).inserted_id
# insert city alarm data
req = urllib2.Request(cityAlarm_url , headers=header)
response = urllib2.urlopen(req).read()
data = json.loads(response)
results = {}
results['acquire_time'] = acquire_time
results['data'] = datetime
collection = db['cityAlarm']
if len(data) > 0:
    post_id = collection.insert_one(results).inserted_id


# insert district alarm data
areas = ['青浦', '松江', '金山', '闵行', '市区', '宝山', '嘉定', '浦东', '奉贤', '崇明']
for area in areas:
    req = urllib2.Request(district_alarm+area, headers=header)
    response = urllib2.urlopen(req).read()
    results = json.loads(response)
    results['acquire_time'] = acquire_time
    collection = db['districtAlarm']
    if len(results['data']) > 0:
        post_id = collection.insert_one(results).inserted_id


