#!/usr/bin/env python
# -*- coding: utf-8 -*-
from ..models import *
from flask.ext.restful import Resource
from sqlalchemy import func
from flask import request
from ..lib.util import *
import datetime
from ..login.views import auth


class countRank(Resource):
    # decorators = [auth.login_required]

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
            user_rank = devData.query.group_by(devData.user_id).count()
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
            temp['count'] = devData.query.filter_by(user_id=id).count()
            temp['username'] = record.username
            ten_rank.append(temp)
        result = {}
        user_infor = {}
        user_infor['count'] = devData.query.filter_by(user_id=id).count()
        user_infor['user_rank'] = user_rank + 1
        result['user_infor'] = user_infor
        for i in range(len(ten_rank)):
            ten_rank[i]['user_rank'] = str(i + 1)
        result['ten_rank'] = ten_rank
        return {"status": "success", 'data': result}


class Rank(Resource):
    # decorators = [auth.login_required]

    def get(self):
        user_id = request.args['user_id']
        shows = devData.query.join(
            User, User.id == devData.user_id).join(
            picStr, picStr.user_id == devData.user_id).add_columns(
            User.name, User.username,
            User.province, func.count(devData.user_id)).group_by(
            devData.user_id).order_by(
            func.count(devData.user_id).desc()).all()
        if len(shows) == 0:
            return {"mesge": "暂时无数据"}
        result = {}
        rankBuf = []
        user_rank = 0
        user_count = 0
        for ele in shows:
            temp = {}
            temp['user_id'] = ele[0].user_id
            temp['img'] = picStr.query.filter_by(
                user_id=temp['user_id']).limit(1).first().img
            temp['name'] = ele[1]
            temp['province'] = ele[3]
            temp['username'] = ele[2]
            temp['count'] = ele[4]
            temp['user_rank'] = str(shows.index(ele) + 1)
            if int(temp['user_id']) == int(user_id):
                user_rank = temp['user_rank']
                user_count = ele[4]
            rankBuf.append(temp)
        if user_rank == 0:
            user_rank = len(shows) + 1
        user_infor = {}
        user_infor['user_rank'] = int(user_rank)
        user_infor['count'] = user_count
        ten_rank = rankBuf[:10] if len(rankBuf) > 10 else rankBuf
        result['user_infor'] = user_infor
        result['ten_rank'] = ten_rank
        return {'status': 'success', 'data': result}


class get_bonus(Resource):
    # decorators = [auth.login_required]

    def get(self):
        user_id = request.args['user_id']
        counts_dev = devData.query.filter_by(user_id=user_id).count()
        counts_user = usrData.query.filter_by(id=user_id).count()
        bonus = int((counts_dev ** 0.7 + counts_user ** 0.3) * 10)
        return {'status': 'success', 'data': bonus}


class pageRank(Resource):
    def get(self):
        uid = request.args['user_id']
        users = User.query.all()
        user_ids = []
        for user in users:
            user_ids.append(user.id)
        if len(user_ids) == 0:
            return {'status': 'fail', 'mesg': '无用户注册!'}, 200
        total = []
        for user_id in user_ids:
            records = devData.query.filter_by(
                user_id=user_id).all()
            temp = {}
            if len(records) == 0:
                continue
            else:
                temp['id'] = user_id
                temp['counts'] = len(records)
                total.append(temp)
        result = self.quickSort(total, 0, len(total) - 1)
        rank = 0
        count = 0
        tenRank = []
        if len(result) == 0:
            return {{'status': 'fail', 'mesg': '用户没有上传数据!'}, 200}
        else:
            for i in xrange(len(result)):
                if result[i]['id'] == uid:
                    rank = i + 1
                    count = result[i]['counts']
                    break
            if len(result) > 10:
                tenRank = total[:11]
            else:
                tenRank = result
        rankData = []
        for i in range(len(tenRank)):
            temp = {}
            temp['user_rank'] = i + 1
            temp['counts'] = tenRank[i]['counts']
            record = User.query.filter_by(id=tenRank[i]['id']).first()
            temp['user_id'] = record.id
            temp['username'] = record.username
            temp['province'] = record.province
            temp['name'] = record.name
            rerd = picStr.query.filter_by(
                user_id=record.id).first()
            if rerd is None:
                continue
            temp['img'] = rerd.img
            rankData.append(temp)
        user_infor = {}
        user_infor['count'] = count
        user_infor['user_rank'] = rank
        data = {}
        data['user_infor'] = user_infor
        data['ten_rank'] = rankData
        return {'status': 'success', 'data': data}, 200

    def quickSort(self, arrDict, left, right):
        if left >= right:
            return arrDict
        key = arrDict[left]
        low = left
        high = right
        while left < right:
            while left < right and arrDict[right]['counts'] <= key['counts']:
                right -= 1
            arrDict[left] = arrDict[right]
            while left < right and arrDict[left]['counts'] > key['counts']:
                left += 1
            arrDict[right] = arrDict[left]
        arrDict[left] = key
        self.quickSort(arrDict, low, left - 1)
        self.quickSort(arrDict, left + 1, high)
        return arrDict
