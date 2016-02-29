#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import request
from flask.ext.restful import Resource
from flask.ext.restful import reqparse
from ..models import *
from ..lib.util import *
from ..login.views import auth


class devResource(Resource):
    decorators = [auth.login_required]

    def get(self):
        user_id = request.args['user_id']
        records = device.query.filter_by(user_id=user_id).all()
        if len(records) == 0:
            return {"status": "success", 'mesg': '用户还未购买设备!'}
        dev_mac = []
        for dev in to_json_list(records):
            del dev['id']
            dev_mac.append(dev['device_mac'])
        devices = {}
        devices['dev_mac'] = dev_mac
        return {"status": "success", "data": devices}

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id', type=str)
        parser.add_argument('dev_mac', type=str)
        args = parser.parse_args(strict=True)
        record = device(args['dev_mac'], args['id'])
        try:
            db.session.add(record)
            try:
                db.session.commit()
                return {'status': 'success', 'mesg': '设备添加成功!'}, 200
            except:
                return {'status': 'fail', 'mesg': '设备已经存在!'}, 200
        except:
            user = User.query.filter_by(id=args['id']).first()
            if user.id is None:
                return {'status': 'fail', 'mesg': '用户不存在!'}, 200
            return {'status': 'fail', 'mesg': '错误的访问方法!'}

    def delete(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id', type=str)
        parser.add_argument('dev_mac', type=str)
        args = parser.parse_args(strict=True)
        record = device.query.filter(
            device.user_id == args['id'],
            device.device_mac == args['dev_mac']).first()
        try:
            db.session.delete(record)
            db.session.commit()
            return {'status': 'success', 'mesg': "删除设备成功!"}
        except:
            dev = device.query.filter_by(device_mac=args['dev_mac']).first()
            if dev is None:
                return {'status': 'fail', 'mesg': '设备不存在!!'}
            return {'status': 'fail', 'mesg': "删除设备失败!"}

    def put(self):
        pass
