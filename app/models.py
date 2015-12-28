#!/usr/bin/env python
# -*- coding: utf-8 -*-
from passlib.apps import custom_app_context as pwd_context
from itsdangerous import (
    TimedJSONWebSignatureSerializer as
    Serializer, BadSignature, SignatureExpired)
from . import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(500), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    birthday = db.Column(db.String(100), nullable=False)
    province = db.Column(db.String(100), nullable=False)
    district = db.Column(db.String(100), nullable=False)
    sex = db.Column(db.Integer, nullable=False)

    img = db.relationship('Img', backref='user', lazy='dynamic')
    device = db.relationship('device', backref='user', lazy='dynamic')
    user_data = db.relationship('usrData', backref='user', lazy='dynamic')
    dev_data = db.relationship('devData', backref='user', lazy='dynamic')
    friends = db.relationship('friends', backref='user', lazy='dynamic')
    usersetting = db.relationship(
        'userSetting', backref='user', lazy='dynamic')
    sport_data = db.relationship('sport', backref='user', lazy='dynamic')

    def __init__(
            self, username, password, email, name,
            birthday, province, district, sex):
        self.username = username
        self.hash_password(password)
        self.email = email
        self.name = name
        self.birthday = birthday
        self.province = province
        self.district = district
        self.sex = sex

    def hash_password(self, password):
        self.password_hash = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)

    def generate_auth_token(self, expiration=60):
        s = Serializer('SECRET_KEY', expires_in=expiration)
        return s.dumps({'id': self.id})

    # only if the token is verified, can the user know the result
    @staticmethod
    def verify_auth_token(token):
        s = Serializer('SECRET_KEY')
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None  # valid token, but expired
        except BadSignature:
            return None  # invalid token
        user = User.query.get(data['id'])
        return user

    def __repr__(self):
        return '<User %r>' % self.username


class reltiWeather(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    datetime = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    sitenumber = db.Column(db.String(255), nullable=False)
    tempe = db.Column(db.String(255), nullable=False)
    humi = db.Column(db.String(255), nullable=False)
    wind_direction = db.Column(db.String(255), nullable=False)
    wind_speed = db.Column(db.String(255), nullable=False)
    pressure = db.Column(db.String(255), nullable=False)
    rain = db.Column(db.String(255), nullable=False)
    visibility = db.Column(db.String(255), nullable=False)

    def __init__(self, datetime, name, sitenumber, tempe,
                 humi, wind_direction, wind_speed, pressure, rain, visibility):
        self.datetime = datetime
        self.name = name
        self.sitenumber = sitenumber
        self.tempe = tempe
        self.humi = humi
        self.wind_direction = wind_direction
        self.wind_speed = wind_speed
        self.pressure = pressure
        self.rain = rain
        self.visibility = visibility


class reltiAqi(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    datetime = db.Column(db.String(255), nullable=False)
    aqi = db.Column(db.String(255), nullable=False)
    level = db.Column(db.String(255), nullable=False)
    pripoll = db.Column(db.String(255), nullable=False)
    content = db.Column(db.String(255), nullable=False)
    measure = db.Column(db.String(255), nullable=False)

    def __init__(self, datetime, aqi, level, pripoll, content, measure):
        self.datetime = datetime
        self.aqi = aqi
        self.level = level
        self.pripoll = pripoll
        self.content = content
        self.measure = measure


class foreWeather(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    datatime = db.Column(db.String(255), nullable=False)
    view_time = db.Column(db.String(255), nullable=False)
    direction = db.Column(db.String(255), nullable=False)
    speed = db.Column(db.String(255), nullable=False)
    tempe = db.Column(db.String(255), nullable=False)
    weather = db.Column(db.String(255), nullable=False)
    weatherpic = db.Column(db.String(255), nullable=False)
    area = db.Column(db.String(255), nullable=False)

    def __init__(self, datatime, view_time, direction,
                 speed, tempe, weather, weatherpic, area):
        self.datatime = datatime
        self.view_time = view_time
        self.direction = direction
        self.speed = speed
        self.tempe = tempe
        self.weather = weather
        self.weatherpic = weatherpic
        self.area = area


class cityAlarm(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    publishtime = db.Column(db.String(255))
    type = db.Column(db.String(255))
    level = db.Column(db.String(255))
    content = db.Column(db.Text)

    def __init__(self, publishtime, type, level, content):
        self.publishtime = publishtime
        self.type = type
        self.level = level
        self.content = content


class device(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    device_mac = db.Column(db.String(255), unique=True)

    def __init__(self, device_mac, user_id):
        self.device_mac = device_mac
        self.user_id = user_id


class devData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    datatime = db.Column(db.String(255), nullable=False)
    device_mac = db.Column(db.String(255), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    longitude = db.Column(db.String(255), nullable=False)
    latitude = db.Column(db.String(255), nullable=False)
    temperature = db.Column(db.String(255), nullable=False)
    humidity = db.Column(db.String(255), nullable=False)
    pressure = db.Column(db.String(255), nullable=False)
    uvIndex = db.Column(db.String(255), nullable=False)

    def __init__(self, datatime, device_mac, user_id, longitude,
                 latitude, temperature, humidity, pressure, uvIndex):
        self.datatime = datatime
        self.device_mac = device_mac
        self.user_id = user_id
        self.longitude = longitude
        self.latitude = latitude
        self.temperature = temperature
        self.humidity = humidity
        self.pressure = pressure
        self.uvIndex = uvIndex


class usrData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    datatime = db.Column(db.String(255), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    longitude = db.Column(db.String(255), nullable=False)
    latitude = db.Column(db.String(255), nullable=False)
    weather = db.Column(db.String(255))
    tempe = db.Column(db.String(255))
    humi = db.Column(db.String(255))
    pressure = db.Column(db.String(255))
    uvIndex = db.Column(db.String(255))
    content = db.Column(db.Text)

    def __init__(self, datatime, user_id, longitude, latitude,
                 weather, tempe, humi, pressure, uvIndex, content):
        self.datatime = datatime
        self.user_id = user_id
        self.longitude = longitude
        self.latitude = latitude
        self.weather = weather
        self.tempe = tempe
        self.humi = humi
        self.pressure = pressure
        self.uvIndex = uvIndex
        self.content = content


class Img(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer, db.ForeignKey('user.id'), unique=True, nullable=False)
    img_path = db.Column(db.String(255), nullable=False)

    def __init__(self, user_id, img_path):
        self.user_id = user_id
        self.img_path = img_path


class friends(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    friend_id = db.Column(db.Integer, nullable=False)

    def __init__(self, user_id, friend_id):
        self.user_id = user_id
        self.friend_id = friend_id


class weaStation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    datetime = db.Column(db.String(255), nullable=False)
    site_name = db.Column(db.String(255), nullable=False)
    tempe = db.Column(db.String(255), nullable=False)
    rain = db.Column(db.String(255), nullable=False)
    humi = db.Column(db.String(255), nullable=False)
    air_press = db.Column(db.String(255), nullable=False)
    wind_direction = db.Column(db.String(255), nullable=False)
    wind_speed = db.Column(db.String(255), nullable=False)
    vis = db.Column(db.String(255), nullable=False)

    def __init__(self, site_name, tempe, rain, humi, air_press,
                 wind_direction, wind_speed, vis):
        self.site_name = site_name
        self.tempe = tempe
        self.rain = rain
        self.humi = humi
        self.air_press = air_press
        self.wind_direction = wind_direction
        self.wind_speed = wind_speed
        self.vis = vis


class site_infor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    site_number = db.Column(db.String(255), nullable=False)
    site_name = db.Column(db.String(255), nullable=False)
    district = db.Column(db.String(255))
    longitude = db.Column(db.String(255), nullable=False)
    latitude = db.Column(db.String(255), nullable=False)
    addr = db.Column(db.String(255))

    def __init__(self, site_number, site_name,
                 district, longitude, latitude, addr):
        self.site_number = site_number
        self.site_name = site_name
        self.district = district
        self.longitude = longitude
        self.latitude = latitude
        self.addr = addr


class userSetting(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),
                        unique=True, nullable=False)
    tempe_H = db.Column(db.String(255))
    tempe_L = db.Column(db.String(255))
    humi_H = db.Column(db.String(255))
    humi_L = db.Column(db.String(255))
    pressure_H = db.Column(db.String(255))
    pressure_L = db.Column(db.String(255))

    def __init__(self, tempe_H, tempe_L, humi_H,
                 humi_L, pressure_H, pressure_L):
        self.tempe_H = tempe_H
        self.tempe_L = tempe_L
        self.humi_H = humi_H
        self.humi = humi_L
        self.pressure_H = pressure_H
        self.pressure_L = pressure_L


class sport(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    datatime = db.Column(db.String(255), nullable=False)
    device_mac = db.Column(
        db.String(255), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    longitude = db.Column(db.String(255), nullable=False)
    latitude = db.Column(db.String(255), nullable=False)
    temperature = db.Column(db.String(255), nullable=False)
    humidity = db.Column(db.String(255), nullable=False)
    pressure = db.Column(db.String(255), nullable=False)
    uvIndex = db.Column(db.String(255), nullable=False)
    distance = db.Column(db.String(255), nullable=False)

    def __init__(self, datatime, device_mac, user_id, longitude,
                 latitude, temperature, humidity, pressure, uvIndex, distance):
        self.datatime = datatime
        self.device_mac = device_mac
        self.user_id = user_id
        self.longitude = longitude
        self.latitude = latitude
        self.temperature = temperature
        self.humidity = humidity
        self.pressure = pressure
        self.uvIndex = uvIndex
        self.distance = distance
