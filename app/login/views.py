#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import g, jsonify
from flask.ext.restful import Resource
from flask.ext.restful import reqparse
from flask.ext.httpauth import HTTPBasicAuth
from flask import request
import random
import httplib
import urllib
from ..lib.util import *
from ..models import *
from . import Login
auth = HTTPBasicAuth()


class userView(Resource):
    # decorators = [auth.login_required]

    def get(self, id):
        user = User.query.filter_by(id=id).first()
        if user is None:
            return {'status': 'fail', "mesg": "该用户不存在!"}
        userInfor = {}
        userInfor['username'] = user.username
        userInfor['email'] = user.email
        userInfor['birthday'] = user.birthday
        userInfor['province'] = user.province
        userInfor['name'] = user.name
        userInfor['district'] = user.district
        userInfor['sex'] = user.sex
        return {'status': 'success', "data": userInfor}, 200

    def delete(self, id):
        pass


class perInfor(Resource):
    # decorators = [auth.login_required]

    def get(self, id):
        user = User.query.filter_by(id=id).first()
        if user is None:
            return {'status': 'fail', "mesg": "该用户不存在!"}
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
        record = picStr.query.filter_by(user_id=str(user.id)).first()
        if record is None:
            return {'status': 'fail', 'mesg': '头像已经迁移'}, 200
        userInfor['img'] = record.img
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

    # @auth.login_required
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


@Login.route('/v1/login/try', methods=['GET'])
@auth.login_required
def login():
    token = g.user.generate_auth_token()
    return jsonify({'token': token.decode('ascii'),
                    'status': 'ok', 'user_id': g.user.id})


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
        mobile = urllib.quote(args['username'])
        exit = User.query.filter_by(username=args['username']).first()
        if exit is not None:
            return {'status': 'fail', "mesg": "手机号已被注册"}, 200
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
        code = verTab.query.filter_by(username=args['username']).first()
        if code.verCode != args['verCode']:
            return {'status': 'fail', "mesg": "验证码错误"}, 200
        record = User(args['username'], args['password'],
                      '', '', '', '', '', '')
        try:
            db.session.add(record)
            db.session.commit()
            user_id = record.id
            img = 'aVZCT1J3MEtHZ29BQUFBTlNVaEVVZ0FBQUpBQUFBQ1FDQVlBQUFEblJ1SzRBQUFBQVhOU1IwSUFyczRjNlFBQUNrZEpSRUZVZUFIdG5RbFQ0a2dVeDF0RlVRUVJ4SE1ZSEoyOXYvOW4yWFYzUEJoR1ZoeEU1UVpGM1A1bk4xVVV5NUVRU1BKL2RGZWx3cEZPdWwvLzB1ZDdyMWVxMWNhN01zRklZRVlKck00WXowUXpFckFrWUFBeUlIaVNnQUhJay9oTVpBT1FZY0NUQkF4QW5zUm5JaHVBREFPZUpHQUE4aVErRTlrQVpCandKQUVEa0NmeG1jZ0dJTU9BSndrWWdEeUp6MFEyQUJrR1BFbkFBT1JKZkNheUFjZ3c0RWtDQmlCUDRqT1JEVUNHQVU4U01BQjVFcCtKYkFBeURIaVNnQUhJay9oTVpBT1FZY0NUQkF4QW5zUm5JaHVBREFPZUpHQUE4aVErRTlrQVpCandKQUVEa0NmeG1jZ0dJTU9BSndsRVBNVW1qdHpyOVZTcjFWYk5aa3QxdXkvVzhmTHlxbnE5dnVyMysrcjl2ZjlmN2xiVTZ1cXFpa1J3YktqTnpZaUtScVA2SEZXSnhMYmEyTmdnbG9MM3BLOHNpMjM4Ky91N2FqU2E2dm01WmgzdGRzZTc5UFFkSXBHSVNpWVRhbmMzcVkrRVdsdGJtOHQ5V1c0aUhpRFVLdVh5by9yK3ZhSmVYMThXV2k2cnF5c3FuZDVWaDRjWnRiMjl2ZEJuaGVYbVlnSHE5VjdWN2UyOWVuaDR0Sm9rdndVZWp5ZFVMbmVvNHZHNDM0LzI5WGtpQVNxVkhqUThkeHFjTjErRk9lcGhlM3U3NnZRMGF6VjFvLzVuLzAwVVFPZ1kzOXg4VTA5UDFWQ1ZDenJhUC83NFNUZHJzVkNsYXg2SkVRTVFSbE5mdnVUVnk4dGkrem16Q2gwanVXejJTQjBkSGN4NmkxREdFd0VRYXB5cnE2K0I5SFhjbG1vbWsxYm41em0zMFVKN1BmMUVZcVBSb0lFSEZLQlRYeWpjaFJZSXR3bWpCcWpUNmFnLy83eWhxSGtHQzZaVXVsZWxVbm53SjlyUHRBQ2h3M3h4Y2EzZTNvSWZhYzFTK29WQ1VYZjJhN05FRFZVY1dvQ0t4VkpvTzh4T1N4Z1FoV0dxd1dsNlIxMUhDVkNyMWJKbWwwZGxpT20zYnJlcmlzWHZURW4rWDFvcEFjcm44ZWJhaTUzL3l4UFZEL2YzWllXK0hHdWdBNmhlYjFxTG9xd0NIMDQzWGdUbURqVWRRQmdHU3d1VlNwVzJScVVDQ0NPdXg4Y25hZnpva1dRdmRNc3ZUb1ZNQlZDMVd0ZkNsdEgzR1M0ZzFpRTlGVURRSUpRYVdQTkdCUkR6YUdVYStGZ0U3dmY1Tms2aUFxamREdWRLK3pRNG5QeVAwZGpMUzlmSnBhRzZoZ29nS1hNLzR3aGdYSlloQTRpdmloOEh5Nmpmb2ZqUEZxZ0FVb3BQd0c2QUlPUkhVUUhFK0lhNkFZaXhpYVlDaUhHVTRnWWdwVmJjWFI2Q3E2a0FndDJWNUFDOWFiWkFsZUwxZGRtVzJKRUluMVVyRlVCcmErdHNMNmlyOURLYVJWTUJ0TDVPbFZ4WDhPQml4aHFXcWtRWUJleVVJamhwV0ZuaDYrTlJBUlNOeW5XbEFwY3hqSUVLSUltbXdUWTAyOXViOWtlcU14VkFzWmc4MjNLYmxxMnRMZnNqMVprS0lBeHoxOWRsTm1PbUJ2THB2WW5IT2QvVVNlTEJCR0lzeHBrdnFob0loUUFQWU5KQ01oblhmaGo1SmhGUkRuUUFKWk03bHROTFNSQ2xVcnd2QlIxQTZBZmhqWlVTMEh6QlFTZHJvQU1JZ3Q3ZDVYMWpoMEhaMllscjkzZWN6UmZ5UWdtUUpMMGc5cnpRQVZTck5iU0RwdUx3aTB6N0hiWnVwUkt2Z3dVcWdPRHorZktTdzVXZEc2SnZiMHUwdm9Lb0FJSlBJUGgvbGhhZ3lucDlYYUIwbGtVREVQYXpxRlRrMmNYYkx3UHM0K0ZObnkzUUFJUytENlBTdVJzZzBCOWlDelFBMWVzTk50bTZUaTg4enJJRkdvRGdWRk42Z05WSnI4ZmxOSlFHSUVKbFBlbThXL21qQVVpcUdzY2daV3RyRWJwWmFScUFKR3NqMmhBeDZnVFJBSlJLeVZ1RnQ4R3h6NHlyOGpRQXdXb0JXMHBLRGRBSHd0NWliSUVHSUFnMm16MFJwd3RrQTNOOHZFKzVLUjBWUU5ncCtlQmd6NWE1bUROTWVvNk85aW56UXdVUUpJeGFTRktIR2c0amZ2amhsSGEzWnpxQUlIQnNIeG1KeUxDVFB6MzlTUDFDMEFHRVdnaDdrUDc4OHhsbG53SHB0OFBIajhkcWZ6OXRmNlU4VXdJRVNhTVorL1hYYzIwbnhsY1RRUTg2bC91Z2pvOFBLYUVaVERUOW5xbndyM3g1V2RBYnNIQXNSR0syK2ZQbm5KNlMyQmtzQjlyUHREV1FMWEUwWnovOWRLWU44OEp2OW95NXJOOSsreXdHSHBRQlBVRElCS3dhZnZubExQVE4yZGxaVHJIYXdFUE9vNElJZ0pBeGpNclFyd2hyd0ZJTURtbEJERUFvbUhRNnFkL3djTHBKT1RrNWtzYU9sUjlSQU1IRFZ4Z0xLcFZLVXMvMVRDSmZGRURJS0dxaGFEUmN0ZERKQ2Y5d2ZSeEU0Z0Q2dHhZNkdKZGYzMytINmJLa3BaZGhBWW9EQ0JuTVpGTFdiUFZ3Wm9QNC91R0R6TDZQTFV1UkFLRVdPanpNMkhrTTdCeVB4MVVpSWNlVHlDaEJpZ1FJR1lYYUIyWjlnd3pROFpFZXhBSUVyKytIaDhFdFZHS0dYTXB5eGFTWFFDeEF5UFRlWG1wUzNoZjZIMWJaR1IySHV4V0thSUN3YkJEVWtINFphaC9BSmhvZ1pEQ2Q5bDhSSHlxcWtvZnVrS3NkeEFPVVNQaS8vcFJJaEY4endBYkE2MWs4UUxHWS8zdFFoSFU5emlzc28rS0xCeWlJUGJpazZHdVBBbWI0Ti9FQUJURVNrcjQxNXlCRTRnRUtZcVBlSUo0NVdLaCtmaFlQVUJBK0ZlRU1kRm1DZUlDYXpZN3ZaZGxxTlgxL1psQVBGQS9RMDFQVmQ5bFdxMDMxK2lyZm94b0VLeHFnWnJPbEhoLzk5K3phNzcrcHYvKys5eDNjSUI0b0ZpRFlpMzM1a2c5Q3B0WXp5K1dLaHZjNXNPZjc5V0NSQU1HbjlCOS9YQ3RBRkZTd25ZYy9QL3ZmaFBxWlozRUFkYnNkZFhGeHJYQU9PZ0FpYk0xUXFjaXRpZWhObXdjaGFUYWI2cSsvOHJvREc3NWhOQndwU0xDRkg1UTNQb3NCQ0c5NVB2OHQxUHROWkRKcDllbFRWcFNYTlhxQTBFeGcreWVXZlNhZ293U0hVbElXWEtrQmFyZGJ1by94VGJYYjdlR2FOZFRmNFZEejlQUUR2VzhnMmlZTXRVNnhlSy91Nzh2VUc3REFadXo4L0tNMlFmSmY1V1JlYnhoZERWU3IxZFhOemEwZVpYWG5KWU5BN3dOblV6REhocE5OeGxWOEdvRGdRQW83KzJIYko0a0JhckF3Z1laUlpCQXFLTFBLTlBRQVlUa0N5d0pCckduTktsUXY4V0FFa00wZVdUYitEQ0NGRWlEMGNRQk11ZnlvYXh5K1RkaThBR1RIUlkyMHY3K25EU1JUb2ZaSUd5cUFPcDJPaHFhaWp5ZTliOVp5ckdiYndJdzdvNDhFRTZHRGc0eENwenRzSVZDQXNHYzZabytyMVlhMWEzR3IxUXFiZkVLVkhuaWtUU1lUVnZNR20vc2c5TDJIQmVJN1FGam9iRFJhR3BxcWVuNnVtNXBtdUVRY2ZrZk5GSS9IZE8yMHE2R0txYzNOclVBNjN3c0hDQ3ZpR0RuVjYwMTlib1ppa2ROaEdWRmRCa2NTT3pzeERWVmNuN2N0cjdWK2RNTG5EaENVcVdvMTFEQTFxNFlKdzZvNEZRbHpTaXlBUW5QMzd4RmZtTCtrdVFCa2o1cXdyenRHVGN0a2xUQ244bDc0YldLeExkMTNTbGw3a2tXakczTjduaWVBTUVmejhQQ29qMmU5Q201R1RYTXJsUVhlQ0gwbmpPYWdHUURubjE2YnVaa0FRa2U0V0x6VDRQaXZiN3hBMlM3ZHJhRVpnRVZkTDlNRHJnRENzQnV6d25kMzM2a1hNWmVPbENrWmhnUDBYQzZyWGVHNGI5b2NBNFIrenVWbFhuZU1hMU9TWS81bWxJQzloWmJiclJnYzZVUmpWdmppNHNyQXcwaUd3elJqdXVYMzN5OWQ3M3JrQ0tDcnE3eSs4ZkpZV3pxVXViakwzdDdlZEVWeG8rZnFuRnV6VEFVSXVzWllhakJoT1NTQWVieEM0ZFp4WmljQ2hLYnI2OWVpNDV1WkMyVkk0T21wNWxoOVppSkFkM2RsdlZZVlBoTVpHY1VVN2x3VUNuZU9FamdSb0dVd3pYVWtwU1c4Q0V0UVRyWVJIUXNRWnBtbDZCMHZZZm5QSmN0T3RFREhBZ1NWQ3hPV1d3TDErblFHeGdJRVJTOFRsbHNDVVBERDZzT2tNQmFnVHNmNVhNQ2tCNWovZUNVQXJZcHBmZ2JHQXJSTWZ2NTRpM2p4S1ovbUltY3NRRmo3TXNGSVlKcHUxejl6ekgyL2NVZEMrQUFBQUFCSlJVNUVya0pnZ2c9PQ=='
            inti_img = picStr(str(record.id), img)
            db.session.add(inti_img)
            db.session.commit()
            return {'status': 'success', "mesg": "用户注册成功!",
                    "data": {"userId": user_id}}, 200
        except:
            return {'status': 'fail', 'mesg': '用户注册失败!'}, 200


class chPasswd(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', type=str)
        args = parser.parse_args(strict=True)
        mobile = urllib.quote(args['username'])
        exit = User.query.filter_by(username=args['username']).first()
        if exit is None:
            return {'status': 'fail', "mesg": "手机号输入错误"}, 200
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


class imgRes(Resource):
    def get(self):
        user_id = request.args['user_id']
        record = picStr.query.filter_by(user_id=user_id).first()
        if record is None:
            return {'status': 'fail', 'mesg': "账号错误"}, 200
        return {'status': 'success', 'img': record.img}, 200

    def put(self):
        parser = reqparse.RequestParser()
        parser.add_argument('user_id', type=str)
        parser.add_argument('img', type=str)
        args = parser.parse_args(strict=True)
        record = picStr.query.filter_by(user_id=args['user_id'])
        if record is None:
            return {'status': 'fail', 'mesg': "账号错误"}, 200
        record.img = args['img']
        try:
            db.session.add(record)
            db.session.commit()
            return {'status': 'success', 'mesg': '头像更新成功'}
        except:
            return {'status': 'fail', 'mesg': '头像更新失败'}

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('user_id', type=str)
        parser.add_argument('img', type=str)
        args = parser.parse_args(strict=True)
        record = picStr(args['user_id'], args['img'])
        try:
            db.session.add(record)
            db.session.commit()
            return {'status': 'success', 'mesg': '图像插入成功'}
        except:
            return {'status': 'fail', 'mesg': '头像插入失败'}
