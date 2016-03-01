#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask.ext.restful import Resource
from flask.ext.restful import reqparse
from ..models import *
from ..lib.util import *
from ..login.views import auth


class viewSet(Resource):
    # decorators = [auth.login_required]

    def put(self):
        parser = reqparse.RequestParser()
        parser.add_argument('user_id', type=str)
        parser.add_argument('tempe_H', type=str)
        parser.add_argument('tempe_L', type=str)
        parser.add_argument('humi_H', type=str)
        parser.add_argument('humi_L', type=str)
        parser.add_argument('pressure_H', type=str)
        parser.add_argument('pressure_L', type=str)
        args = parser.parse_args(strict=True)
        user_id = args['user_id']
        record = userSetting.query.filter_by(user_id=user_id).first()
        if record is None:
            buf = userSetting(args['user_id'], args['tempe_H'], args['tempe_L'], args['humi_H'],
                              args['humi_L'], args['pressure_H'], args['pressure_L'])
            db.session.add(buf)
            try:
                db.session.commit()
                return {'status': 'success', 'mesg': '信息设置成功!'}
            except:
                return {'status': 'fail', 'mesg': '信息设置失败!'}
        else:
            record.tempe_H = args['tempe_H']
            record.tempe_L = args['tempe_L']
            record.humi_L = args['humi_L']
            record.humi_H = args['humi_H']
            record.pressure_H = args['pressure_H']
            record.pressure_L = args['pressure_L']
            try:
                db.session.commit()
                return {'status': 'success', 'mesg': '信息更新成功!'}
            except:
                return {'status': 'fail', 'mesg': '信息更新失败!'}


class feed(Resource):
    # decorators = [auth.login_required]

    def get(self):
        record = feedBack.query.filter_by(
            handle=0).order_by(feedBack.post_time).limit(500)
        if record is None:
            return {"status": "fail", "mesg": "用户未给出反馈"}
        result = []
        for item in to_json_list(record):
            del item['handle']
            del item['handle_time']
            result.append(item)
        return {"status": "获取反馈成功", "data": result}

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('user_id', type=str)
        parser.add_argument('advice')
        parser.add_argument('post_time', type=str)
        args = parser.parse_args(strict=True)
        record = feedBack(
            args['user_id'], args['advice'], args['post_time'], 0)
        db.session.add(record)
        try:
            db.session.commit()
            return {"status": "success", "mesg": "数据上传成功!"}
        except:
            user = User.query.filter_by(id=args['user_id']).first()
            if user is None:
                return {"status": "fail", "mesg": "用户还未注册!"}
            return {"status": "fail", "mesg": "数据上传失败"}

    def put(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id', type=str)
        parser.add_argument('handle_time', type=str)
        parser.add_argument('handle', type=str)
        args = parser.parse_args(strict=True)
        record = feedBack.query.filter_by(id=args['id']).first()
        if record is None:
            return {"status": "fail", "mesg": "用户未给出反馈"}
        record.handle_time = args['handle_time']
        record.handle = args['handle']
        try:
            db.session.commit()
            return {"status": "success", "mesg": "反馈已解决!"}
        except:
            return {'status': 'fail', 'mesg': '数据更新失败'}
