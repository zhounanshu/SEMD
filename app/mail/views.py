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
        paser.add_argument('suggestion', type=str)
        args = paser.parse_args(strict=True)
        content = args['suggestion']
        msg = Message(content, recipients=["marvinzns@163.com"])
        msg.body = "testing"
        msg.html = "<b>testing</b>"
        mail.send(msg)
        return {'staus': 'ok'}
