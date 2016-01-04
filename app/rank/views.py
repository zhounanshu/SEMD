#!/usr/bin/env python
# -*- coding: utf-8 -*-
from ..models import *
from flask.ext.restful import Resource
from sqlalchemy import func
from flask import request
from ..lib.util import *


class countRank(Resource):

    def get(self):
        user_id = request.args['user_id']
        shows = devData.query.group_by(devData.user_id).order_by(
            func.count(devData.user_id).desc()).all()
        if len(shows) == 0:
            return {"mesge": "暂时无数据"}
        rank_container = []
        for show in shows:
            rank_container.append(show.user_id)
        if int(user_id) not in rank_container:
            user_rank = -1
        else:
            user_rank = rank_container.index(int(user_id))
        ten_rank = []
        buf = []
        if len(rank_container) < 10:
            buf = rank_container
        else:
            buf = rank_container[: 10]
        for id in buf:
            temp = {}
            record = User.query.filter_by(id=id).first()
            temp['user_id'] = id
            temp['username'] = record.username
            ten_rank.append(temp)
        result = {}
        result['user_rank'] = user_rank + 1
        result['ten_rank'] = ten_rank
        return {"status": "success", 'data': result}


class get_bonus(Resource):

    def get(self):
        user_id = request.args['user_id']
        counts_dev = devData.query.filter_by(user_id=user_id).count()
        counts_user = usrData.query.filter_by(id=user_id).count()
        bonus = int((counts_dev ** 0.7 + counts_user ** 0.3) * 10)
        return {'status': 'success', 'data': bonus}
