#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import g, jsonify
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
            return {'status': 'fail', "mesg": "该用户不存在!"}
        return {'status': 'success', "data": userInfor}, 200

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
            try:
                db.session.commit()
            except:
                return {'status': 'fail', "mesg": "用户名已被注册!"}, 200
            user_id = record.id
            return {'status': 'success', "mesg": "用户注册成功!",
                    "data": {"userId": user_id}}, 200
        except:
            return {'status': 'fail', 'mesg': '用户注册失败!'}

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
            return {'status': 'fail', "mesg": "用户名不可修改!"}
        user.hash_password(args['password'])
        user.birthday = args['birthday']
        user.name = args['name']
        user.email = args['email']
        user.province = args['province']
        user.sex = args['sex']
        user.district = args['district']
        try:
            db.session.commit()
            return {'status': 'success', "mesg": "用户信息更新成功"}, 200
        except:
            return {'status': 'fail', "mesg": "更新失败!"}, 200


class verify_login(Resource):

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', type=str)
        parser.add_argument('password', type=str)
        args = parser.parse_args(strict=True)
        user = User.query.filter_by(username=args['username']).first()
        if not user:
            return {'status': 'fail', 'mesg': '用户名输入错误!'}
        if not user.verify_password(args['password']):
            return {'status': 'fail', 'mesg': '密码输入错误!'}
        token = user.generate_auth_token()
        return {'status': 'success', 'data': {'token': token.decode('ascii'),
                                              'status': 'ok'}, 'mesg': '登录成功'}


@Login.route('/v1/token', methods=['GET'])
@auth.login_required
def get_auth_token():
    token = g.user.generate_auth_token()
    return jsonify({'token': token.decode('ascii')})


# @Login.route('/v1/login', methods=['GET'])
# @auth.login_required
# def login():
#     token = g.user.generate_auth_token()
#     return jsonify({'token': token.decode('ascii'), 'status': 'ok'})


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
