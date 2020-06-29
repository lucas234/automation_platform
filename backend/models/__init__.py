# coding=utf-8
# auther：Liul5
# date：9/20/2019 11:14 AM
# tools：PyCharm
# Python：3.7.3
from datetime import datetime
from common.utils import dump_datetime
from db import db


class BaseModel(db.Model):
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    is_active = db.Column(db.Integer, default=1, doc="标志位，是否删除", comment="标志位，是否删除, 0表示逻辑删除")
    created_at = db.Column(db.DateTime, default=datetime.now(), doc="创建时间", comment="创建时间")
    modified_at = db.Column(db.DateTime, doc="更新时间", comment="更新时间")
    # 需要隐藏的字段
    _hidden_fields = ["is_active", "modified_at"]

    @classmethod
    def default_hidden_fields(cls):
        return cls._hidden_fields

    def from_json(self, **kwargs):
        """更新数据以json格式的数据"""
        _dict = self.__dict__
        for key in kwargs:
            if key in _dict:
                setattr(self, key, kwargs[key])

    def to_json(self):
        """返回json格式的数据"""
        hidden = self._hidden_fields if hasattr(self, "_hidden_fields") else []
        hidden.extend(["_sa_instance_state"])
        _dict = self.__dict__
        # 设置时间格式
        _time = ["created_at", "modified_at"]
        for i in _time:
            _dict[i] = dump_datetime(_dict.get(i, None))
        # _dict["created_at"] = dump_datetime(_dict["created_at"])
        # _dict["modified_at"] = dump_datetime(_dict["modified_at"])

        # 删除需要隐藏的字段
        for i in hidden:
            if i in _dict:
                del _dict[i]
        return _dict

