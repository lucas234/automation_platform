# coding=utf-8
# auther：Liul5
# date：9/16/2019 4:25 PM
# tools：PyCharm
# Python：3.7.3
from flask_restful import Api
from flask import Blueprint
from resources.v2.user import UserApi


def register_resource_views(app):
    api = Api(app)
    api.add_resource(UserApi, '/users', '/users/add', endpoint="add_user")
    api.add_resource(UserApi, '/users/<int:user_id>', endpoint="retrieve_user")
    api.add_resource(UserApi, '/users/<string:username>', endpoint="delete_user")


def register_blueprints_v2(app):
    # 注册版本
    """
    注册蓝图->v1版本
    """
    bp_v2 = Blueprint('v2', __name__)
    register_resource_views(bp_v2)
    app.register_blueprint(bp_v2, url_prefix='/api/v2')
