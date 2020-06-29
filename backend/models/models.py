# coding=utf-8
# auther：Liul5
# date：9/16/2019 1:38 PM
# tools：PyCharm
# Python：3.7.3
from passlib.apps import custom_app_context as pwd_context
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous.exc import SignatureExpired, BadSignature
from config import run_config
from models import BaseModel
from db import db


class User(BaseModel):
    # 自定义表名（如果不指定表名，默认为model类名的小写（user））
    __tablename__ = 'users'
    username = db.Column(db.String(120), unique=True, nullable=False, doc="用户名", comment="用户名")
    password = db.Column(db.String(120), nullable=False, doc="密码", comment="密码")
    role = db.Column(db.Integer, default=0, doc="角色", comment="角色, 0表示普通用户，1 表示admin")

    email = db.Column(db.String(20), doc="邮箱", comment="邮箱")
    address = db.Column(db.String(250), doc="地址", comment="地址")
    phone = db.Column(db.String(20), doc="手机号", comment="手机号")
    gender = db.Column(db.Integer, doc="性别", comment="性别, 0表示女性，1 表示男性")
    tech = db.Column(db.String(250), doc="擅长领域", comment="擅长领域")
    api = db.relationship("ApiModel", backref='api', lazy=True)

    # 需要隐藏的字段
    _hidden_fields = ["password"] + BaseModel.default_hidden_fields()

    @staticmethod
    def hash_password(password):
        return pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password)

    def generate_auth_token(self, expiration=600):
        s = Serializer(run_config.SECRET_KEY, expires_in=expiration)
        return s.dumps({'id': self.id})

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(run_config.SECRET_KEY)
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None  # valid token, but expired
        except BadSignature:
            return None  # invalid token
        user = User.query.get(data['id'])
        return user


class ApiModel(BaseModel):
    __tablename__ = 'apis'
    name = db.Column(db.String(120), doc="用例名称", comment="用例名称")
    description = db.Column(db.String(120), doc="用例描述", comment="用例描述")
    project = db.Column(db.String(20), doc="所属项目名称", comment="所属项目名称")
    method = db.Column(db.String(20), doc="请求方法", comment="请求方法")
    url = db.Column(db.String(120), doc="请求URL", comment="请求URL")
    # result = db.Column(db.String(120), doc="测试结果", comment="测试结果")
    header = db.Column(db.String(120), doc="请求头", comment="请求头")
    body = db.Column(db.String(120), doc="请求参数体", comment="请求参数体")
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, doc="执行者id", comment="执行者id")
    user = db.relationship("User", backref='users', lazy=True)
    status = db.Column(db.Integer, default=1, doc="状态，是否启用", comment="状态，是否启用, 0表示禁用")
    imp = db.Column(db.Integer, default=1, doc="优先级", comment="优先级, 1,2,3表示3表示最高")
    tags = db.Column(db.String(70), doc="标记tag", comment="标记tag,多个用，分隔开")


class Tag(BaseModel):
    """标记测试用例"""
    __tablename__ = 'tags'
    mark = db.Column(db.String(40), doc="用例标志", comment="用例标志")
    api_id = db.Column(db.Integer, db.ForeignKey('apis.id'), nullable=False, doc="接口id", comment="接口id")


class Report(BaseModel):
    """记录测试结果"""
    __tablename__ = 'reports'
    name = db.Column(db.String(120), doc="用例名称", comment="用例名称")
    api_id = db.Column(db.Integer, db.ForeignKey('apis.id'), nullable=False, doc="接口id", comment="接口id")
    # api = db.relationship("ApiModel", backref='apis', lazy=True)
    result = db.Column(db.String(120), doc="测试结果", comment="测试结果")
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, doc="执行者id", comment="执行者id")
    # operator = db.Column(db.String(30), doc="执行者", comment="执行者")
    status = db.Column(db.Integer, default=1, doc="运行结果状态", comment="1表示成功，0表示失败，2表示跳过，3表示异常")
