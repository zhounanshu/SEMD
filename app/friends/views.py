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
            friend_infor['id'] = person.user.id
            friend_infor['name'] = person.user.name
            names.append(friend_infor)
        temp = {}
        temp['friends'] = names
        return temp, 200

    def post(self):
        paser = reqparse.RequestParser()
        paser.add_argument('id', type=str)
        paser.add_argument('friendname', type=str)
        args = paser.parse_args(strict=True)
        friend = User.query.filter_by(username=args['friendname']).first()
        if friend is None:
            return {'mesg': '该好友还未注册!'}
        exit = friends.query.filter(friends.user_id == args['id'],
                                    friends.friend_id == friend.id).first()
        if exit is not None:
            return {'mesg': '已经是朋友!'}
        if args['id'] == str(friend.id):
            return {'mesg': '不能和自己成为好友!'}
        record = friends(args['id'], friend.id)
        try:
            db.session.add(record)
            db.session.commit()
            return {'mesg': '成功添加好友!'}
        except:
            return {'mesg': '添加好友失败!'}

    def delete(self):
        paser = reqparse.RequestParser()
        paser.add_argument('id', type=str)
        paser.add_argument('friendname', type=str)
        args = paser.parse_args(strict=True)
        friend = User.query.filter_by(username=args['friendname']).first()
        if friend.id is None:
            return {'mesg': '该好友还未注册!'}
        friendShip = friends.query.filter(
            friends.user_id == args['id'],
            friends.friend_id == friend.id).first()
        try:
            db.session.delete(friendShip)
            db.session.commit()
            return {'mesg': '成功删除好友!'}
        except:
            return {'mesg': '删除好友失败!'}

    def put(self):
        pass
