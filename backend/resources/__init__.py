# coding=utf-8
# auther：Liul5
# date：9/27/2019 3:45 PM
# tools：PyCharm
# Python：3.7.3
from flask import g
from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth, MultiAuth
from models.models import User

basic_auth = HTTPBasicAuth()
token_auth = HTTPTokenAuth(scheme='Bearer')
multi_auth = MultiAuth(token_auth, basic_auth)


# @basic_auth.verify_password
# def verify_password(username, password):
#     user = User.query.filter_by(username=username).first()
#     if not user or not user.verify_password(password):
#         return False
#     g.user = user
#     return True
#
#
# @token_auth.verify_token
# def verify_token(token):
#     user = User.verify_auth_token(token)
#     if not user:
#         return False
#     g.user = user
#     return True


# 用上边两个，或者这一个
@token_auth.verify_token
@basic_auth.verify_password
def verify_password(username_or_token, password=None):
    # first try to authenticate by token
    user = User.verify_auth_token(username_or_token)
    if not user:
        # try to authenticate with username/password
        user = User.query.filter_by(username=username_or_token).first()
        if not user or not user.verify_password(password):
            return False
    g.user = user
    # g.token = username_or_token
    return True
