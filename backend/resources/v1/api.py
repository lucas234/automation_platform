# coding=utf-8
# auther：Liul5
# date：10/15/2019 11:20 AM
# tools：PyCharm
# Python：3.7.3
import time
from datetime import datetime
from flask import request, jsonify
from flask_restful import Resource, reqparse
from resources.forms.api_form import ApiForm
from models.models import ApiModel, User, Tag
from db import session_add, db, session_commit, session_delete
from common.utils import response, get_not_exist_fields, sort_id


class ApiResource(Resource):
    def post(self):
        api_data = request.get_json()
        not_exist_fields = get_not_exist_fields(api_data.keys(), ApiModel)
        if not_exist_fields:
            return response(f"Unknown arguments: {not_exist_fields}", 404)
        form = ApiForm(data=api_data)
        if form.validate():
            new_api = ApiModel(**api_data)
            session_add(new_api)
            msg = session_add(new_api)
            if msg:
                return response(f"{msg}", 500)
            else:
                return response("api add successfully at {0}".format(time.strftime("%Y-%m-%d %H:%M:%S")))
        return response(form.errors, 400)

    def get(self, api_id):
        try:
            api_ = ApiModel.query.filter_by(id=api_id).first()
            if api_:
                return jsonify(response(api_.to_json()))
            else:
                return response('api does`t exists', 400)
        except Exception as e:
            return response(f"{e}", 500)

    def put(self, api_id):
        api_data = request.get_json()
        not_exist_fields = get_not_exist_fields(api_data.keys(), ApiModel)
        if not_exist_fields:
            return response(f"Unknown arguments: {not_exist_fields}", 404)
        api_ = ApiModel.query.filter_by(id=api_id).first()
        if not api_:
            return response('api does`t exists', 400)
        # 直接修改字段is_active，逻辑删除
        # api_.from_json(**{"is_active": 0})
        api_data['modified_at'] = datetime.now()
        api_.from_json(**api_data)
        msg = session_commit()
        if not msg:
            return response()
        else:
            return response(f"{msg}", 400)

    def delete(self, api_id):
        try:
            # 直接物理删除数据
            flag = ApiModel.query.filter_by(id=api_id).delete()
            session_commit()
            if flag:
                return response()
            else:
                return response(f'api {api_id}(id) does`t exists', 400)
        except Exception as e:
            return response(f'{e}', 500)


class ApiListResource(Resource):
    """获取全部的api"""
    parser = reqparse.RequestParser()

    def get(self):
        try:
            # 联表查询
            # 左外连接设置 isouter=True 或者直接使用 outerjoin
            query = db.session.query(User.username, ApiModel.url, ApiModel.id,
                                     ApiModel.status, ApiModel.name, ApiModel.created_at,
                                     ApiModel.description, ApiModel.body, ApiModel.header,
                                     ApiModel.imp, ApiModel.project, ApiModel.method, ApiModel.tags). \
                outerjoin(User, ApiModel.user_id == User.id)  # .join(Tag, ApiModel.id == Tag.api_id, isouter=True)
            # print([dict(zip(result.keys(), result)) for result in results])
            self.parser.add_argument('page', type=int, help='The page must be int type', required=True)
            self.parser.add_argument('per_page', type=int, help='The per_page must be int type', required=True)
            self.parser.add_argument('sort', type=str, help='The sort must be string type')
            self.parser.add_argument('name', type=str, help='The name must be string type')
            data = self.parser.parse_args(strict=True)  # 获取传输的值/strict=True代表设置如果传以上未指定的参数主动报错
            page = data['page']
            per_page = data['per_page']
            sort = data.get('sort', None)
            name = data.get('name', None)
            if page < 1:
                return response("The page must be larger than 1", 400)
            if sort:
                apis = query.filter(ApiModel.is_active == 1).order_by(sort_id(sort, ApiModel)).paginate(page, per_page)
            else:
                apis = query.filter(ApiModel.is_active == 1).paginate(page, per_page)
            if name:
                apis = query.filter(ApiModel.is_active == 1, ApiModel.name == name).order_by(sort_id(sort, ApiModel)).paginate(page, per_page)
            if apis:
                resp_data = {
                    "page": apis.page,
                    "pages": apis.pages,
                    "per_page": apis.per_page,
                    "has_prev": apis.has_prev,
                    "has_next": apis.has_next,
                    "total": apis.total,
                    'api_list': [dict(zip(result.keys(), result)) for result in apis.items]
                }
                return jsonify(response(resp_data))
            else:
                return response('api does`t exists', 400)
        except Exception as e:
            return response(f"{e}", 500)
