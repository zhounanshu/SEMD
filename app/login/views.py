#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import jsonify, g
from flask.ext.restful import Resource
from flask.ext.restful import reqparse
from flask.ext.httpauth import HTTPBasicAuth

from ..lib.util import *
from ..models import *
from . import Login
auth = HTTPBasicAuth()


class userView(Resource):

    def get(self, id):
        user = User.query.filter_by(id=id).first()
        userInfor = {}
        userInfor['username'] = user.username
        userInfor['email'] = user.email
        userInfor['birthday'] = user.birthday
        userInfor['province'] = user.province
        userInfor['district'] = user.district
        userInfor['sex'] = user.sex
        if user is None:
            return {"error": "该用户不存在!"}
        return {"data": userInfor}, 200

    def delete(self, id):
        pass


class user(Resource):

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', type=str)
        parser.add_argument('password', type=str)
        parser.add_argument('birthday', type=str)
        parser.add_argument('name')
        parser.add_argument('email', type=str)
        parser.add_argument('province')
        parser.add_argument('sex', type=str)
        parser.add_argument('district')
        args = parser.parse_args(strict=True)
        record = User(args['username'], args['password'],
                      args['email'], args['name'], args['birthday'],
                      args['province'], args['district'], args['sex'])
        try:
            db.session.add(record)
            db.session.commit()
            user_id = record.id
            return {"mesg": "用户注册成功!", "userId": user_id}, 200
        except:
            user = User.query.filter_by(username=args['username']).first()
            if user is not None:
                return {"mesg": "用户名已被注册!"}, 400
            return {'mesg': '用户注册失败!'}

    def put(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id', type=str)
        parser.add_argument('username', type=str)
        parser.add_argument('password', type=str)
        parser.add_argument('birthday', type=str)
        parser.add_argument('name')
        parser.add_argument('email', type=str)
        parser.add_argument('province')
        parser.add_argument('sex', type=str)
        parser.add_argument('district')
        args = parser.parse_args(strict=True)
        user = User.query.filter_by(id=args['id']).first()
        if user.username != args["username"]:
            return {"mesg": "用户名不可修改!"}
        user.hash_password(args['password'])
        user.birthday = args['birthday']
        user.name = args['name']
        user.email = args['email']
        user.province = args['province']
        user.sex = args['sex']
        user.district = args['district']
        try:
            db.session.commit()
            return {"mesg": "用户信息更新成功"}, 200
        except:
            return {"mesg": "更新失败!"}, 400


@Login.route('/v1/token', methods=['GET'])
@auth.login_required
def get_auth_token():
    token = g.user.generate_auth_token()
    return jsonify({'token': token.decode('ascii')})


@Login.route('/v1/login', methods=['GET'])
@auth.login_required
def login():
    token = g.user.generate_auth_token()
    return jsonify({'token': token.decode('ascii'), 'status': 'ok'})


@auth.verify_password
def verify_password(username_or_token, password):
    # first try to authenticate by token
    user = User.verify_auth_token(username_or_token)
    if not user:
        # try to authenticate with username/password
        user = User.query.filter_by(username=username_or_token).first()
        if not user or not user.verify_password(password):
            return False
    g.user = user
    return True
