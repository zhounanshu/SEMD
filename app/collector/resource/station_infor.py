#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
sys.path.append('..')
from lib.common import *
import csv

f = file('../atomation.csv', 'rb')
reader = csv.reader(f)
fields = ['site_number', 'site_name',
          'district', 'latitude', 'longitude', 'addr']
for line in reader:
    line = ','.join(line).decode('gb2312')
    line = line.split(',')[1:]
    storeData('site_infor', dict(zip(fields, line)))
