#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask.ext.restful import Resource
from flask.ext.restful import reqparse
from flask_mail import Message
from .. import mail


class sendMail(Resource):
    def post(self):
        paser = reqparse.RequestParser()
        paser.add_argument('phone', type=str)
        paser.add_argument('suggestion')
        args = paser.parse_args(strict=True)
        msg = Message(
            '意见反馈',
            recipients=["bobozns@126.com"])
        msg.body = args['suggestion']
        msg.html = "<b>" + args['suggestion'] + "</b>"
        mail.send(msg)
        return {'staus': 'ok'}
