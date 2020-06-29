# coding=utf-8
# auther：Liul5
# date：9/17/2019 2:00 PM
# tools：PyCharm
# Python：3.7.3
from flask_restful import reqparse, Resource
from flask import g, jsonify
import time
from flask import request
from resources.forms.login_form import LoginForm
from resources.forms.register_form import RegisterForm
from common.utils import response, get_not_exist_fields
from datetime import datetime
from models.models import User
from db import session_commit, session_add, session_delete
from resources import basic_auth, token_auth, multi_auth


class UserApi(Resource):
    parser = reqparse.RequestParser()

    @token_auth.login_required
    def get(self, user_id):
        try:
            user = User.query.filter_by(id=user_id).first()
            if user:
                return jsonify(user.to_json())
            else:
                return {'msg': 'user does`t exists'}, 400
        except Exception as e:
            return {"errors": f"{e}", 'msg': "user retrieval failed at {}".format(time.strftime("%Y-%m-%d %H:%M:%S"))}, 500

    def post(self):
        self.parser.add_argument('username', type=str, help='This username cannot be blank', required=True)
        self.parser.add_argument('password', type=str, help='This password cannot be blank', required=True)
        data = self.parser.parse_args(strict=True)  # 获取传输的值/strict=True代表设置如果传以上未指定的参数主动报错
        if User.query.filter_by(username=data['username']).filter_by(is_active=1).first():
            return {'msg': 'user {} already exists'.format(data['username'])}, 400
        new_user = User(username=data['username'], password=User.hash_password(data['password']))
        msg = session_add(new_user)
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
                user.modified_at = datetime.now()
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
                return {"msg": "user delete: {1} success at {0}".format(time.strftime("%Y-%m-%d %H:%M:%S"), username)}
            else:
                return {'msg': f'user {username} does`t exists'}, 400
        except Exception as e:
            return {"errors": f"{e}", 'msg': "user delete {1} failure at {0}".format(time.strftime("%Y-%m-%d %H:%M:%S"), username)}, 500


class UserToken(Resource):
    parser = reqparse.RequestParser()

    @multi_auth.login_required
    def get(self):
        token = g.user.generate_auth_token()
        return jsonify({'token': token.decode('ascii')})

    def post(self):
        self.parser.add_argument('username', type=str, help='This username cannot be blank', required=True)
        self.parser.add_argument('password', type=str, help='This password cannot be blank', required=True)
        data = self.parser.parse_args(strict=True)  # 获取传输的值/strict=True代表设置如果传以上未指定的参数主动报错
        try:
            user = User.query.filter_by(username=data['username']).first()
            if user:
                if not user.verify_password(data['password']):
                    return {"msg": "the username or password is wrong!"}, 403
                token = user.generate_auth_token()
                user_info = user.to_json()
                user_info.update({'token': token.decode('ascii')})
                return jsonify(user_info)
            else:
                return {"msg": "the username or password is wrong!"}, 403
        except Exception as e:
            return {"errors": f"{e}", 'msg': "user login failed at {0}".format(time.strftime("%Y-%m-%d %H:%M:%S"))}, 500

# base wtf form


class LoginResource(Resource):

    parser = reqparse.RequestParser()

    @multi_auth.login_required
    def get(self):
        token = g.user.generate_auth_token()
        return jsonify({'token': token.decode('ascii')})

    def post(self):
        user_data = request.get_json()
        not_exist_fields = get_not_exist_fields(user_data.keys(), User)
        if not_exist_fields:
            return response(f"Unknown arguments: {not_exist_fields}", 404)
        form = LoginForm(data=user_data)
        if form.validate():
            user = form.get_user()
            token = user.generate_auth_token()
            user_info = user.to_json()
            user_info.update({'token': token.decode('ascii')})
            # login_user(user, remember=form.remember.data)
            return jsonify({'status': 'success', 'data': user_info})
        return {'status': 'error', 'message': form.errors}, 404


class UserResource(Resource):
    # 通过decorators字段为整个类里面的接口添加授权
    # decorators = [token_auth.login_required]

    @token_auth.login_required
    def get(self, user_id):
        try:
            user = User.query.filter_by(id=user_id).first()
            if user:
                return jsonify(response(user.to_json()))
            else:
                return response('user does`t exists', 400)
        except Exception as e:
            return response(f"{e}", 500)

    def delete(self, user_id):
        try:
            # 直接物理删除数据
            flag = User.query.filter_by(id=user_id).delete()
            if flag:
                session_commit()
                return response(f"delete {user_id} successfully")
            else:
                return response(f'user {user_id} does`t exists', 400)
        except Exception as e:
            return response(f"{e}", 500)

    def put(self, user_id):
        data = request.get_json()
        try:
            not_exist_fields = get_not_exist_fields(data.keys(), User)
            if not_exist_fields:
                return response(f"Unknown arguments: {not_exist_fields}", 404)
            user = User.query.filter_by(id=user_id).first()
            if not user:
                return response(f'user {user_id} does`t exists', 400)
            # 直接修改字段is_active，逻辑删除
            # user.from_json(**{"is_active": 0})
            user.from_json(**data)
            user.modified_at = datetime.now()
            msg = session_commit()
            if not msg:
                return response()
            else:
                return response(f"{msg}", 400)
        except Exception as e:
            return response(f"{e}", 500)

    def post(self):
        user_data = request.get_json()
        not_exist_fields = get_not_exist_fields(user_data.keys(), User)
        if not_exist_fields:
            return response(f"Unknown arguments: {not_exist_fields}", 404)
        form = RegisterForm(data=user_data)
        user_data['password'] = User.hash_password(user_data['password'])
        if form.validate():
            new_user = User(**user_data)
            session_add(new_user)
            msg = session_add(new_user)
            if msg:
                return response(f"{msg}", 500)
            else:
                return response("user create successfully")
        return response(form.errors, 400)


class UserListResource(Resource):
    """获取全部的user"""
    parser = reqparse.RequestParser()

    def get(self):
        try:
            self.parser.add_argument('page', type=int, help='The page must be int type', required=True)
            self.parser.add_argument('per_page', type=int, help='The per_page must be int type', required=True)
            data = self.parser.parse_args(strict=True)  # 获取传输的值/strict=True代表设置如果传以上未指定的参数主动报错
            page = data['page']
            per_page = data['per_page']
            if page < 1:
                return response("The page must be larger than 1", 400)
            users = User.query.paginate(page, per_page)
            if users:
                resp_data = {
                    "page": users.page,
                    "pages": users.pages,
                    "per_page": users.per_page,
                    "has_prev": users.has_prev,
                    "has_next": users.has_next,
                    "total": users.total,
                    'api_list': [i.to_json() for i in users.items]
                }
                return jsonify(response(resp_data))
            else:
                return response('user does`t exists', 400)
        except Exception as e:
            return response(f"{e}", 500)
