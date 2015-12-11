#!/usr/bin/env pyhton
# -*- coding: utf-8 -*-
import sys
import MySQLdb
sys.path.append('..')
from config import *
import logging

FORMAT = '%(asctime)s %(name)-6s %(levelname)-6s %(message)s'
logging.basicConfig(level=logging.DEBUG,
                    format=FORMAT,
                    datefmt="%a, %d %b %Y %H:%M:%S")


def storeData(table, value):
    try:
        conn = MySQLdb.connect(host=host, charset='utf8',
                               user=user, passwd=passwd, port=port, db=db)
        cur = conn.cursor()
        fields = '('
        s_fields = '('
        temp = []
        count = 0
        for key in value.keys():
            count += 1
            fields += key
            s_fields += '%s'
            if count == len(value):
                fields += ') values'
                s_fields += ')'
            else:
                fields += ','
                s_fields += ','
            temp.append(value[key])
        sql = 'insert into ' + table
        sql += fields
        sql += s_fields
        cur.execute(sql, temp)
        conn.commit()
        cur.close()
        conn.close()
    except:
        logging.debug("insert data failed......")
