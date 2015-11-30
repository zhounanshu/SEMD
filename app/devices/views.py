#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import request
from flask.ext.restful import Resource
from flask.ext.restful import reqparse
from ..models import *
from ..lib.util import *


class devResource(Resource):

    def get(self):
        user_id = request.args['user_id']
        records = device.query.filter_by(user_id= user_id).all()
        if len(records) == 0:
            return {'mesg': '用户还未购买设备!'}
        dev_mac = []
        for dev in to_json_list(records):
            del dev['id']
            dev_mac.append(dev['device_mac'])
        devices = {}
        devices['macId'] = dev_mac
        return devices, 200

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id', type=str)
        parser.add_argument('macId', type=str)
        args = parser.parse_args(strict=True)
        record = device(args['macId'], args['id'])
        try:
            db.session.add(record)
            try:
                db.session.commit()
                return {'mesg': '设备添加成功!'}, 200
            except:
                return {'mesg': '设备已经存在!'}, 400
        except:
            user = User.query.filter_by(id=args['id']).first()
            if user.id is None:
                return {'mesg': '用户不存在!'}, 400
            return {'mesg': '错误的访问方法!'}

    def delete(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id', type=str)
        parser.add_argument('macId', type=str)
        args = parser.parse_args(strict=True)
        record = device.query.filter(
            device.user_id == args['id'],
            device.device_mac == args['macId']).first()
        try:
            db.session.delete(record)
            db.session.commit()
            return {'mesg': "删除设备成功!"}, 200
        except:
            dev = device.query.filter_by(device_mac=args['macId']).first()
            if dev.id is None:
                return {'mesg': '设备不存在!!'}
            return {'mesg': "删除设备失败!"}

    def put(self):
        pass
