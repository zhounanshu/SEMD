#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import urllib2
import json
import datetime
sys.path.append('..')
from lib.common import *

response = urllib2.urlopen(aqi_real).read()
response = json.loads(response)
time_str = filter(str.isalnum,
                  response['datetime'].encode('utf-8'))
year = int(time_str[0: 4])
month = int(time_str[4: 6])
day = int(time_str[6: 8])
hour = int(time_str[8:])

response['datetime'] = datetime.datetime(
    year, month, day, hour).strftime('%Y-%m-%d %H:%M:%S')
storeData('relti_aqi', response)
