#!/usr/bin/env python
# -*- coding: utf-8 -*-
import urllib2
import json
import sys
import os
import tempfile
import re

reload(sys)
# sys.setdefaultencoding("utf-8")
# url = 'localhost'
# header = {"Accept": " application/json", "Content-Type": " application/json"}
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

# basedir = os.path.split(os.path.realpath(__file__))[0]


# def delete_file_folder(src):
#     if os.path.isfile(src):
#         try:
#             os.remove(src)
#         except:
#             pass
#     if os.path.isdir(src):
#         for item in os.listdir(src):
#             itemsrc = os.path.join(src, item)
#             print itemsrc
#             delete_file_folder(itemsrc)
#         try:
#             os.rmdir(src)
#         except:
#             pass
l = ['阴', '多云']
pic_str = '阴有的雨转多云多云有的雨'
pic_buf = []
reg = r'有.*?雨'
pattern = re.compile(reg)
special = re.findall(pattern, pic_str)
temp = []
print len(special)
for a in special:
    temp.append((a.decode('utf8')[0]+ a.decode('utf8')[-1]).encode('utf8'))
for n in temp:
    print n
for f in l:
    if pic_str.find(f) != -1:
        pic_buf.append(f)
for ele in pic_buf:
    if ele == '有雨':
        pic_buf[pic_buf.index(ele)] = '小雨'
for ele in pic_buf:
    print ele
