# !/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask
from flask.ext.mail import Mail, Message

app = Flask(__name__)
app.config.update(
    DEBUG=True,
    MAIL_SERVER='smtp.163.com',
    MAIL_PROT=25,
    MAIL_USE_TLS=True,
    MAIL_USE_SSL=False,
    MAIL_USERNAME='marvinzns@163.com',
    MAIL_PASSWORD='wangy2013',
    MAIL_DEBUG=True
)

mail = Mail(app)


@app.route('/')
def index():
    msg = Message("Hi!This is a test ", sender='marvinzns@163.com',
                  recipients=['bobozns@126.com'])
    msg.body = "This is a first email"
    mail.send(msg)
    print "Mail sent"
    return "Sent"

if __name__ == "__main__":
    app.run()

