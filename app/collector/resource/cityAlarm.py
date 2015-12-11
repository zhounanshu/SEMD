#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import urllib2
import json
sys.path.append('..')
from lib.common import *

header = {"Accept": " application/json",
          "Content-Type": " application/json"}
req = urllib2.Request(cityAlarm_url, headers=header)
response = urllib2.urlopen(req).read()
result = json.loads(response)
if len(result) != 0:
    storeData('city_alarm', result)
