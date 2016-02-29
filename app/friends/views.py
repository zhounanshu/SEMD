#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask.ext.restful import Resource
from flask.ext.restful import reqparse
from flask import request
from ..models import *
from ..lib.util import *
from .. import URI
from ..login.views import auth


class friend(Resource):
    decorators = [auth.login_required]

    def get(self):
        user_id = request.args['user_id']
        friend = friends.query.filter_by(user_id=user_id).all()
        if len(friend) == 0:
            return {'friends': []}, 200
        names = []
        for person in friend:
            friend_infor = {}
            friend_infor['id'] = person.friend_id
            friend_infor['name'] = User.query.filter_by(
                id=person.friend_id).first().name
            friend_infor['username'] = User.query.filter_by(
                id=person.friend_id).first().username
            names.append(friend_infor)
        temp = {}
        temp['friends'] = names
        return {'status': 'success', 'data': temp}

    def post(self):
        paser = reqparse.RequestParser()
        paser.add_argument('id', type=str)
        paser.add_argument('friendname', type=str)
        args = paser.parse_args(strict=True)
        friend = User.query.filter_by(username=args['friendname']).first()
        if friend is None:
            return {'status': 'fail', 'mesg': '该好友还未注册!'}
        exit = friends.query.filter(friends.user_id == args['id'],
                                    friends.friend_id == friend.id).first()
        if exit is not None:
            return {'status': 'fail', 'mesg': '已经是朋友!'}
        if args['id'] == str(friend.id):
            return {'status': 'fail', 'mesg': '不能和自己成为好友!'}
        record = friends(args['id'], friend.id)
        try:
            db.session.add(record)
            db.session.commit()
            return {'status': 'success', 'mesg': '成功添加好友!'}
        except:
            return {'status': 'fail', 'mesg': '添加好友失败!'}

    def delete(self):
        paser = reqparse.RequestParser()
        paser.add_argument('id', type=str)
        paser.add_argument('friendname', type=str)
        args = paser.parse_args(strict=True)
        friend = User.query.filter_by(username=args['friendname']).first()
        if friend.id is None:
            return {'status': 'fail', 'mesg': '该好友还未注册!'}
        friendShip = friends.query.filter(
            friends.user_id == args['id'],
            friends.friend_id == friend.id).first()
        try:
            db.session.delete(friendShip)
            db.session.commit()
            return {'status': 'success', 'mesg': '成功删除好友!'}
        except:
            return {'status': 'fail', 'mesg': '删除好友失败!'}

    def put(self):
        pass


class searchFriend(Resource):
    decorators = [auth.login_required]

    def get(self):
        name = request.args['username']
        users = User.query.filter(
            User.username.ilike("%" + name + "%")).all()
        result = []
        if len(users) == 0:
            return {'status': 'success', 'data': result}
        else:
            for user in users:
                username = user.username
                result.append(username)
            return {'status': 'success', 'data': result}


class searchFrid(Resource):
    decorators = [auth.login_required]

    def get(self):
        name = request.args['username']
        id = str(request.args['id'])
        users = User.query.filter(
            User.username.ilike("%" + name + "%")).all()
        result = []
        if len(users) == 0:
            return {'status': 'success', 'data': result}, 200
        else:
            for user in users:
                buf = {}
                buf['name'] = user.name
                buf['img'] = URI + str(user.id)
                buf['area'] = user.province + user.district
                buf['friend_id'] = str(user.id)
                beFri = friends.query.filter(
                    friends.user_id == id,
                    friends.friend_id == str(user.id)).first()
                if beFri is not None:
                    continue
                else:
                    record = application.query.filter(
                        application.friend_id == str(user.id),
                        application.user_id == id).first()
                    if record is None:
                        record = application.query.filter(
                            application.user_id == str(user.id),
                            application.friend_id == id).first()
                        if record is None:
                            # 添加状态
                            buf['append'] = '1'
                        else:
                            continue
                    else:
                            # 待确认状态
                        buf['append'] = '0'
                result.append(buf)
            return {'status': 'success', 'data': result}, 200


class usrApply(Resource):
    decorators = [auth.login_required]

    def post(self):
        paser = reqparse.RequestParser()
        paser.add_argument('id', type=str)
        paser.add_argument('friend_id', type=str)
        paser.add_argument('text')
        args = paser.parse_args(strict=True)
        record = application.query.filter(
            application.user_id == args['id'],
            application.friend_id == args['friend_id']).first()
        if record is None:
            record = application(
                args['friend_id'], args['id'], args['text'], '0', '1')
        try:
            db.session.add(record)
            db.session.commit()
            return {'status': 'success', 'mesg': '好友申请成功!'}
        except:
            return {'status': 'fail', 'mesg': '好友申请失败!'}

    # 好友申请获取
    def get(self):
        friend_id = request.args['id']
        applicants = application.query.filter_by(
            friend_id=friend_id).order_by('id desc').all()
        result = []
        if len(applicants) == 0:
            return {'status': 'success', 'result': result}
        for applicant in applicants:
            record = User.query.filter_by(id=applicant.user_id).first()
            buf = {}
            buf['img'] = URI + str(record.id)
            buf['area'] = record.province + record.district
            buf['name'] = record.name
            buf['text'] = applicant.text
            buf['friend_id'] = str(record.id)
            buf['pass'] = applicant.handled
            if applicant.visible == '0':
                continue
            result.append(buf)
        return {'status': 'success', 'result': result}

    def put(self):
        paser = reqparse.RequestParser()
        paser.add_argument('id', type=str)
        paser.add_argument('friend_ids', type=str, action='append')
        args = paser.parse_args(strict=True)
        for item in args['friend_ids']:
            record = application.query.filter(
                application.friend_id == args['id'],
                application.user_id == item).first()
            if record.handled == '1':
                record.visible = '0'
                db.session.add(record)
                db.session.commit()
            else:
                db.session.delete(record)
                db.session.commit()
        return {'status': 'success', 'mesg': '清理成功'}, 200


class approv(Resource):
    decorators = [auth.login_required]

    def post(self):
        paser = reqparse.RequestParser()
        paser.add_argument('id', type=str)
        paser.add_argument('friend_id', type=str)
        paser.add_argument('approved', type=str)
        args = paser.parse_args(strict=True)
        if args['approved'] == '1':
            record = friends(args['friend_id'], args['id'])
            db.session.add(record)
            db.session.commit()
            record = friends(args['id'], args['friend_id'])
            db.session.add(record)
            db.session.commit()
            record = application.query.filter(
                application.friend_id == args['id'],
                application.user_id == args['friend_id']).first()
            record.handled = '1'
            db.session.add(record)
            db.session.commit()
            return {'status': 'success', 'mesg': '添加好友成功!'}, 200
        else:
            record = application.query.filter(
                application.friend_id == args['id'],
                application.user_id == args['friend_id']).first()
            db.session.delete(record)
            db.session.commit()
            return {'status': 'success', 'mesg': '拒绝申请!'}, 200
