# coding=utf-8
# auther：Liul5
# date：9/19/2019 4:03 PM
# tools：PyCharm
# Python：3.7.3
from views.views import delete_user_by_id


# 通过注册函数的方式
def register_views(app):
    """可在此下随意添加视图"""
    app.add_url_rule('/api/users/<int:user_id>', 'delete_user_by_id', delete_user_by_id, methods=['delete'])
