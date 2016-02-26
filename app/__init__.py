#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from config import config
from flask_mail import Mail
db = SQLAlchemy()
mail = Mail()
URI = 'http://www.zns.link:8083/v1/img/'


def create_app(cnf):
    app = Flask(__name__)
    app.config.from_object(config[cnf])
    config[cnf].init_app(app)
    db.init_app(app)
    mail.init_app(app)

    from .login import Login
    app.register_blueprint(Login)
    from .weather import Weather
    app.register_blueprint(Weather)
    from .devices import Device
    app.register_blueprint(Device)
    from .friends import Friends
    app.register_blueprint(Friends)
    from semd import devMonitor
    app.register_blueprint(devMonitor)
    from .setting import userSet
    app.register_blueprint(userSet)
    from .Img import imgBlueprint
    app.register_blueprint(imgBlueprint)
    from .mycity import myCity_blueprint
    app.register_blueprint(myCity_blueprint)
    from .rank import Ranks
    app.register_blueprint(Ranks)
    from .mail import Advice
    app.register_blueprint(Advice)
    return app
