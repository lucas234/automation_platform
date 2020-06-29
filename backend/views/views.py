# coding=utf-8
# auther：Liul5
# date：9/19/2019 3:40 PM
# tools：PyCharm
# Python：3.7.3
import time
from models.models import User
from db import session_commit, session_delete


def delete_user_by_id(user_id):
    try:
        user = User.query.filter_by(id=user_id).first()
        if user:
            # user.flag = 0
            session_delete(user)
            session_commit()
            return {"msg": "user delete: {1} success at {0}".format(time.strftime("%Y-%m-%d %H:%M:%S"), user_id)}
        else:
            return {'msg': f'user {user_id} does`t exists！'}, 400
    except Exception as e:
        return {"errors": f"{e}", 'msg': "user delete: {1} failure at {0}".format(time.strftime("%Y-%m-%d %H:%M:%S"), user_id)}, 500


# 以路由方式在下面添加的方式
# def register_views(app):
#     """可在此下随意添加视图"""
#     @app.route("/api/users/<int:user_id>", methods=['delete'])
#     def delete_user_by_id(user_id):
#         try:
#             user = User.query.filter_by(id=user_id).first()
#             if user:
#                 # user.flag = 0
#                 session_delete(user)
#                 session_commit()
#                 return {"msg": "user delete: {1} success at {0}".format(time.strftime("%Y-%m-%d %H:%M:%S"), user_id)}
#             else:
#                 return {'msg': f'user {user_id} does`t exists'}, 400
#         except Exception as e:
#             return {"errors": f"{e}", 'msg': "user delete: {1} failure at {0}".format(time.strftime("%Y-%m-%d %H:%M:%S"), user_id)}, 500

