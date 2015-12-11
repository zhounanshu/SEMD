#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import urllib2
import json
sys.path.append('..')
from lib.common import *

header = {"Accept": " application/json",
          "Content-Type": " application/json"}
req = urllib2.Request(forecast_10, headers=header)
response = urllib2.urlopen(req).read()
results = json.loads(response)
for result in results:
    result['view_time'] = result['datatime']
    result['area'] =  '上海'
    storeData('fore_weather', result)
