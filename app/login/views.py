#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import g, jsonify
from flask.ext.restful import Resource
from flask.ext.restful import reqparse
from flask.ext.httpauth import HTTPBasicAuth
import random
import httplib
import urllib
from ..lib.util import *
from ..models import *
from . import Login
from .. import URI
auth = HTTPBasicAuth()


class userView(Resource):

    def get(self, id):
        user = User.query.filter_by(id=id).first()
        userInfor = {}
        userInfor['username'] = user.username
        userInfor['email'] = user.email
        userInfor['birthday'] = user.birthday
        userInfor['province'] = user.province
        userInfor['name'] = user.name
        userInfor['district'] = user.district
        userInfor['sex'] = user.sex
        if user is None:
            return {'status': 'fail', "mesg": "该用户不存在!"}
        return {'status': 'success', "data": userInfor}, 200

    def delete(self, id):
        pass


class perInfor(Resource):

    def get(self, id):
        user = User.query.filter_by(id=id).first()
        userInfor = {}
        userInfor['username'] = user.username
        userInfor['birthday'] = user.birthday
        userInfor['name'] = user.name
        userInfor['area'] = user.province + user.district
        userInfor['sex'] = user.sex
        if user.sex == "":
            userInfor['sex'] = '男'
        if user.birthday == '':
            userInfor['birthday'] = '未设定'
        if user.district == "":
            userInfor['district'] = '未设定'
        if user.province == '':
            userInfor['province'] = '未设定'
        userInfor['id'] = str(user.id)
        userInfor['img'] = URI + str(id)
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
        parser.add_argument('sex')
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
        parser.add_argument('sex')
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
        id = user.id
        return {'status': 'success', 'data': {"user_id": id,
                                              'token': token.decode('ascii')
                                              }, 'mesg': '登录成功'}


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

sms_host = "sms.yunpian.com"
port = 443
# 版本号
version = "v1"
# 智能匹配模版短信接口的URI
sms_send_uri = "/" + version + "/sms/send.json"
apikey = "d9f53a96514423381bc3f315143a810e"


def send_sms(apikey, text, mobile):
    """
    通用接口发短信
    """
    params = urllib.urlencode(
        {'apikey': apikey, 'text': text, 'mobile': mobile})
    headers = {
        "Content-type": "application/x-www-form-urlencoded",
        "Accept": "text/plain"}
    conn = httplib.HTTPSConnection(sms_host, port=port, timeout=30)
    conn.request("POST", sms_send_uri, params, headers)
    response = conn.getresponse()
    response_str = response.read()
    conn.close()
    return response_str


def generate_verification_code():
    code_list = []
    for i in range(6):
        for i in range(10):  # 0-9数字
            code_list.append(str(i))
    myslice = random.sample(code_list, 6)
    verification_code = ''.join(myslice)
    return verification_code


class megVerif(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', type=str)
        args = parser.parse_args(strict=True)
        user = User.query.filter_by(username=args['username']).first()
        if user is not None:
            return {'status': 'fail', "mesg": "用户名已被注册!"}, 200
        # 修改为您要发送的手机号码，多个号码用逗号隔开
        mobile = urllib.quote(args['username'])
        # 修改为您要发送的短信内容
        verCode = generate_verification_code()
        record = verTab.query.filter_by(username=args['username']).first()
        if record is None:
            record = verTab(args['username'], verCode)
        else:
            record.verCode = verCode
        try:
            db.session.add(record)
            db.session.commit()
        except:
            return {'status': 'fail', 'mesg': '验证码发送失败'}, 200
        text = '您的验证码是' + verCode + '【云片网】'
        # 调用智能匹配模版接口发短信
        with open('log.txt', 'a+') as f:
            f.write(send_sms(apikey, text, mobile) + '\n')
        return {'status': 'success', 'mesg': '验证码已经发送'}, 200


class signUp(Resource):

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', type=str)
        parser.add_argument('password', type=str)
        parser.add_argument('verCode', type=str)
        args = parser.parse_args(strict=True)
        exit = User.query.filter_by(username=args['username']).first()
        if exit is not None:
            return {'status': 'fail', "mesg": "手机号已被注册"}, 200
        code = verTab.query.filter_by(username=args['username']).first()
        if code.verCode != args['verCode']:
            return {'status': 'fail', "mesg": "验证码错误"}, 200
        record = User(args['username'], args['password'],
                      '', '', '', '', '', '')
        try:
            db.session.add(record)
            db.session.commit()
            user_id = record.id
            return {'status': 'success', "mesg": "用户注册成功!",
                    "data": {"userId": user_id}}, 200
        except:
            return {'status': 'fail', 'mesg': '用户注册失败!'}, 200


class chPasswd(Resource):
    def put(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username')
        parser.add_argument('password')
        parser.add_argument('verCode')
        args = parser.parse_args(strict=True)
        record = User.query.filter_by(username=args['username']).first()
        if record is None:
            return {'status': 'fail', "mesg": "手机号输入错误"}, 200
        # if record.verify_password(args['password']):
        #     return {'status': 'fail', "mesg": "修改密码不能和原来密码相同"}, 200
        code = verTab.query.filter_by(username=args['username']).first()
        if code.verCode != args['verCode']:
            return {'status': 'fail', "mesg": "验证码错误"}, 200
        try:
            db.session.add(record)
            db.session.commit()
            user_id = record.id
            return {'status': 'success', "mesg": "密码修改成功",
                    "data": {"userId": user_id}}, 200
        except:
            return {'status': 'fail', 'mesg': '密码修改失败'}, 200
