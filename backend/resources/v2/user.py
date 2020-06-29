# coding=utf-8
# auther：Liul5
# date：9/17/2019 2:00 PM
# tools：PyCharm
# Python：3.7.3
from flask_restful import reqparse, Resource
import time
from datetime import datetime
from models.models import User
from db import session_commit, session_add, session_delete


class UserApi(Resource):
    parser = reqparse.RequestParser()

    def get(self, user_id):
        try:
            user = User.query.filter_by(id=user_id).first()
            if user:
                return user.to_json()
            else:
                return {'msg': 'user does`t exists'}, 400
        except Exception as e:
            return {"errors": f"{e}", 'msg': "user retrieval failed at {}".format(time.strftime("%Y-%m-%d %H:%M:%S"))}, 500

    def post(self):
        self.parser.add_argument('username', type=str, help='This username cannot be blank', required=True)
        self.parser.add_argument('password', type=str, help='This password cannot be blank', required=True)
        data = self.parser.parse_args(strict=True) # 获取传输的值/strict=True代表设置如果传以上未指定的参数主动报错
        if User.query.filter_by(username=data['username']).filter_by(flag=1).first():
            return {'msg': 'user {} already exists'.format(data['username'])}, 400
        new_user = User(username=data['username'], password=User.hash_password(data['password']))
        session_add(new_user)
        msg = session_commit()
        if msg:
            return {"errors": f"{msg}", 'msg': "user add failed at {0}".format(time.strftime("%Y-%m-%d %H:%M:%S"))}, 500
        else:
            return {"msg": "user add successfully at {0}".format(time.strftime("%Y-%m-%d %H:%M:%S"))}

    def put(self):
        self.parser.add_argument('username', type=str, help='This username cannot be blank', required=True)
        self.parser.add_argument('password', type=str, help='This password cannot be blank', required=True)
        self.parser.add_argument('new_password', type=str, help='This password cannot be blank', required=True)
        data = self.parser.parse_args()
        try:
            user = User.query.filter_by(username=data['username']).first()
            if user:
                if not user.verify_password(data['password']):
                    return {"msg": "the username or password is wrong!"}, 403
                user.password = User.hash_password(data['new_password'])
                user.update_time = datetime.now()
                msg = session_commit()
                return {"status": msg, "msg": "user update successfully at {0}".format(time.strftime("%Y-%m-%d %H:%M:%S"))}
            else:
                return {'msg': 'user {} does`t exists'.format(data['username'])}, 400
        except Exception as e:
            return {"errors": f"{e}", 'msg': "user update failed at {0}".format(time.strftime("%Y-%m-%d %H:%M:%S"))}, 500

    def delete(self, username):
        try:
            user = User.query.filter_by(username=username).first()
            if user:
                # user.flag = 0
                session_delete(user)
                session_commit()
                return {"msg": "user delete: {1} success at {0}".format(time.strftime("%Y-%m-%d %H:%M:%S"), username)}
            else:
                return {'msg': f'user {username} does`t exists'}, 400
        except Exception as e:
            return {"errors": f"{e}", 'msg': "user delete {1} failure at {0}".format(time.strftime("%Y-%m-%d %H:%M:%S"), username)}, 500

