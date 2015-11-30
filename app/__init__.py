#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from config import config
db = SQLAlchemy()


def create_app(cnf):
    app = Flask(__name__)
    app.config.from_object(config[cnf])
    config[cnf].init_app(app)
    db.init_app(app)

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
    return app
