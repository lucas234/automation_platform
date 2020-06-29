# coding=utf-8
# auther：Liul5
# date：10/24/2019 5:41 PM
# tools：PyCharm
# Python：3.7.3
from flask_restful import Resource
from faker import Faker
from common.utils import response


class FakerDataResource(Resource):
    fake = Faker("zh_CN")

    def get(self):
        info = {"name": self.fake.name(),
                "phone": self.fake.phone_number(),
                "id": self.fake.ssn(min_age=18, max_age=90),
                "email": self.fake.email(),
                "address": self.fake.address(),
                "credit_card": self.fake.credit_card_number(card_type=None),  # 卡号
                "postcode": self.fake.postcode(),
                }
        if info:
            return response(info)
        return response("获取信息失败，请重试！", 400)

    def post(self):
        pass


