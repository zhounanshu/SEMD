#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pymongo import MongoClient
import MySQLdb
import urllib2
import json
import datetime
from config import *

db = MySQLdb.connect(
    host='localhost', user='root', passwd='marvinzns',
    port=3306, db='meteor', charset='utf8')
cursor = db.cursor(MySQLdb.cursors.DictCursor)
cursor.execute('select * from dev_data order by datatime desc limit 1')
data = cursor.fetchone()
url = location_weather + 'jd=' + data['longitude'] + '&' + 'wd=' + data['latitude']
header = {"Accept": " application/json",
          "Content-Type": " application/json"}
req = urllib2.Request(url, headers=header)
response = urllib2.urlopen(req).read()
results = {}
results['data'] = json.loads(response)
results['data']['dev_data'] = data
results['msg'] = '定点天气信息'
results['acquire_time'] = datetime.datetime.now().strftime('%y-%m-%d %H:%M%S')
store data to mongoDB
client = MongoClient('202.121.178.186', 27017)
db = client['meteorShanghai']
collection = db['locationWeather']
post_id = collection.insert_one(results).inserted_id
