#!/usr/bin/env python
# -*- coding: utf-8 -*-
# from flask import Flask
# from flask.ext.mail import Mail, Message

# app = Flask(__name__)
# app.config.update(
#     DEBUG=True,
#     MAIL_SERVER='smtp.163.com',
#     MAIL_PROT=25,
#     MAIL_USE_TLS=True,
#     MAIL_USE_SSL=False,
#     MAIL_USERNAME='marvinzns@163.com',
#     MAIL_PASSWORD='marvin2013',
#     MAIL_DEBUG=True
# )

# mail = Mail(app)


# @app.route('/')
# def index():
#     msg = Message("Hi!This is a test ", sender='marvinzns@163.com',
#                   recipients=['bobozns@126.com'])
#     msg.body = "This is a first email"
#     mail.send(msg)
#     print "Mail sent"
#     return "Sent"

# if __name__ == "__main__":
#     app.run()
import random

def generate_verification_code():
    ''' 随机生成6位的验证码 '''
    code_list = []
    for i in range(6):
        for i in range(10): # 0-9数字
            code_list.append(str(i))
    myslice = random.sample(code_list, 6)
    verification_code = ''.join(myslice)
    # print code_list
    # print type(myslice)
    return verification_code
if __name__ == '__main__':
    code = generate_verification_code()
    print code
