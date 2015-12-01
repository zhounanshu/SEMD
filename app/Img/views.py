#!/usr/bin/env python
# -*- coding: utf-8 -*-
from PIL import Image
from flask.ext.restful import Resource
import os
from flask import request
from flask import send_file
from ..models import *


def compress_img(img, w, h):
    img.thumbnail((w, h))
    img.save('wld.png', 'PNG')
    return img

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])


def get_path():
    basedir = os.path.split(os.path.realpath(__file__))[0]
    return basedir + '/img'


def allowed_file(f):
    return '.' in f and f.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


def delete_file_folder(src):
    if os.path.isfile(src):
        try:
            os.remove(src)
        except:
            pass
    if os.path.isdir(src):
        for item in os.listdir(src):
            itemsrc = os.path.join(src, item)
            print itemsrc
            delete_file_folder(itemsrc)
        try:
            os.rmdir(src)
        except:
            pass


class imgResource(Resource):

    def post(self, id):
        f = request.files['file']
        filename = f.filename
        if f and allowed_file(filename):
            f_name = str(id) + '.' + \
                str('.' in filename and filename.rsplit('.', 1)[1])
            img_path = os.path.join(get_path(), f_name)
            f.save(img_path)
            record = Img(id, img_path)
            db.session.add(record)
            try:
                db.session.commit()
                return {'mesg': '图片上传成功!'}, 200
            except:
                exit = Img.query.filter_by(id=id).first()
                if exit is not None:
                    return {'mesg': '用户上传头像成功'}
                return {'mesg': '图片上传失败!'}, 400
        else:
            if not f:
                return {'mesg': '文件不能为空!'}, 400
            return {'mesg': '图片格式错误!'}, 400

    def put(self, id):
        f = request.files['file']
        if f and allowed_file(f.filename):
            record = Img.query.filter_by(user_id=id).first()
            if record is None:
                return {'mesg': '该用户没有上传头像!'}, 200
            f.save(record.img_path)
            return {'头像更新成功!'}, 201
        return {'头像更新失败!'}, 400

    def get(self, id):
        width = request.args.get('width')
        height = request.args.get('height')
        img_inf = Img.query.filter_by(user_id=id).first()
        if img_inf is None:
            return {'mesg': '用户还未上传头像!'}, 200
        pic = Image.open(img_inf.img_path)
        w, h = pic.size
        if (w < int(width)) or (h < int(height)):
            return {'mesg': '参数不在合理范围!'}, 400
        if (width is not None) and (height is not None):
            pic = pic.resize((int(width), int(height)), Image.ANTIALIAS)
            prefix = os.path.split(os.path.realpath(__file__))[0] + '/buf/'
            postfix = (img_inf.img_path).split('/')[-1]
            path = prefix + postfix
            print prefix
            delete_file_folder(prefix)
            pic.save(path)
        else:
            path = img_inf.img_path
        return send_file(path)

    def delete(self, id):
        record = Img.query.filter_by(user_id=id).first()
        if record is None:
            return {'mesg': '头像不存在!'}
        db.session.delete(record)
        os.remove(record.img_path)
        db.session.commit()
        return {'mesg': '头像已经删除!'}, 200
