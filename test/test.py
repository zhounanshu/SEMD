#!/usr/bin/env python
# -*- coding: utf-8 -*-
import urllib2
import json
import sys
import os
import tempfile

reload(sys)
sys.setdefaultencoding("utf-8")
url = 'http://61.152.122.112:8080/api/v1/auto_stations/master?appid=bFLKk0uV7IZvzcBoWJ1j&appkey=mXwnhDkYIG6S9iOyqsAW7vPVQ5ZxBe'
header = {"Accept":" application/json", "Content-Type": " application/json"}
# request = urllib2.Request(url, headers=header)
# response = urllib2.urlopen(request).read()
# temp = json.loads(response)['data']
# record = {}
# for dic in temp:
#     if dic['name'] == "闵行":
#         record = dic
# invalid_keys = ['sitenumber', 'rain', 'visibility']
# for key in invalid_keys:
#     del record[key]
# print json.dumps(record, ensure_ascii=False)

basedir = os.path.split(os.path.realpath(__file__))[0]
# print basedir

folder = tempfile.mkdtemp()
# print folder


qpf_url = 'http://61.152.122.112:8080//traffic_api/qpf/000'
req = urllib2.Request(qpf_url, headers=header)
respon = urllib2.urlopen(req).read()
temp = json.loads(respon)['data']
print temp
result = []
for buf in temp:
    if buf['data'] != 0:
        result.append(buf)
print result
