#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import urllib2
import json
sys.path.append('..')
from lib.common import *

header = {"Accept": " application/json",
          "Content-Type": " application/json"}
req = urllib2.Request(station_real, headers=header)
response = urllib2.urlopen(req).read()
results = json.loads(response)['data']
for reslut in results:
    storeData('wea_station', reslut)
