#!/usr/bin/env pyhton
# -*- coding: utf-8 -*-
import re
import urllib2
import os


def getHtml(url):
    page = urllib2.urlopen(url)
    html = page.read()
    return html


def getImg(html):
    reg = r'src="(/+.*?\.jpg)"'
    imgre = re.compile(reg)
    imglist = re.findall(imgre, html)
    return imglist


def save_file(path, file_name, data):
    if data is None:
        return None
    if(not path.endswith("/")):
        path = path + "/"
    f = open(path + file_name, "wb")
    f.write(data)
    f.flush()
    f.close()

html = getHtml(
    'http://sj.yamon.cn/MobileHelp.aspx?m=detail&ChannelID=MobileHelp&id=5')

folder = os.path.split(os.path.realpath(__file__))[0][:-5]
pic_folder = os.path.join(folder, 'app/weather/alarm_pic')
url = 'http://sj.yamon.cn'
i = 0
for path in getImg(html):
    img_url = url + path
    img = getHtml(img_url)
    i += 1
    save_file(pic_folder, str(i) + '.jpg', img)
