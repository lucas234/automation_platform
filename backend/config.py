# coding=utf-8
# auther：Liul5
# date：9/20/2019 11:28 AM
# tools：PyCharm
# Python：3.7.3
# https://flask-chs.readthedocs.io/zh_CN/latest/config.html
# https://zhuanlan.zhihu.com/p/24055329
import os


class BaseConfig:
    # Flask settings
    # SERVER_NAME = '10.212.42.180:5000'  # 此种方式读取配置不能设置localhost，如果设置会一直返回404错误
    DEBUG = False  # Do not use debug mode in production, 启动Flask的Debug模式
    SECRET_KEY = os.getenv('SECRET_KEY', 'some-secret-string')

    # 关于上传下载文件
    # 限制上传文件的大小（8M）
    MAX_CONTENT_LENGTH = 8 * 1024 * 1024
    UPLOAD_FOLDER = r'C:\diy\old coding\test\locust demo\backend\tmp_file'
    ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

    # wtf 跨域设置
    # WTF_CSRF_SECRET_KEY = "some-secret-string"
    # WTF_CSRF_FIELD_NAME = "csrf_token"
    WTF_CSRF_ENABLED = False

    # SQLAlchemy settings
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///db.sqlite"


class DevelopmentConfig(BaseConfig):
    DEBUG = True


class TestingConfig(BaseConfig):
    TESTING = True


class ProductionConfig(BaseConfig):
    pass


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig
}

run_config = config['development']

