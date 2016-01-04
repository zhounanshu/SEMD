#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask.ext.restful import Resource
from flask.ext.restful import reqparse
from flask import request
from ..models import *
from ..lib.util import *


class friend(Resource):

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
