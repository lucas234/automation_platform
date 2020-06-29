# coding=utf-8
# auther：Liul5
# date：9/16/2019 1:44 PM
# tools：PyCharm
# Python：3.7.3

from flask import Flask
from common import register_errors
from views import register_views
from resources.v1 import register_blueprints
from db import db
# from resources.v2 import register_blueprints_v2
# from resources.v1 import register_resource_views

app = Flask(__name__)


@app.before_first_request
def create_tables():
    """执行之前先创建所有不存在的表"""
    app.app_context().push()
    db.create_all()


def configure_app(app):
    # 直接写入方式
    # app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
    # app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    # app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
    # app.config['SECRET_KEY'] = 'some-secret-string'

    # 读取配置方式
    from config import run_config
    app.config.from_object(run_config)


def initialize_app(app):
    configure_app(app)
    db.init_app(app)  # 数据库注册到app
    register_errors(app)  # 注册异常信息处理
    register_views(app)  # 注册非resource的视图路由
    # register_resource_views(app)  # 注册resource的路由视图，非蓝图模式
    register_blueprints(app)   # 注册resource的路由视图，蓝图模式
    # register_blueprints_v2(app) # 通过视图来控制api版本，v2只用使用试验


def main():
    initialize_app(app)
    app.run()


if __name__ == '__main__':
    main()
