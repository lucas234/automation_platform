# coding=utf-8
# auther：Liul5
# date：10/24/2019 1:47 PM
# tools：PyCharm
# Python：3.7.3
import time
from flask import request, jsonify
from flask_restful import Resource
from models.models import Report
from db import session_add, session_commit
from common.utils import response, get_not_exist_fields


class ReportResource(Resource):
    def post(self):
        data = request.get_json()
        print(data)
        not_exist_fields = get_not_exist_fields(data.keys(), Report)
        if not_exist_fields:
            return response(f"Unknown arguments: {not_exist_fields}", 404)
        new_report = Report(**data)
        msg = session_add(new_report)
        if msg:
            return response(f"{msg}", 500)
        else:
            return response("report add successfully at {0}".format(time.strftime("%Y-%m-%d %H:%M:%S")))

    def get(self, report_id):
        try:
            report = Report.query.filter_by(id=report_id).first()
            if report:
                return jsonify(response(info=report.to_json()))
            else:
                return response('report does`t exists', 400)
        except Exception as e:
            return response(f"{e}", 500)

    def delete(self, report_id):
        try:
            flag = Report.query.filter_by(id=report_id).delete()
            msg = session_commit()
            if msg:
                return response(f"{msg}", 500)
            if flag:
                return response()
            else:
                return response(f'report {report_id}(id) does`t exists', 400)

        except Exception as e:
            return response(f"{e}", 500)


class ReportListResource(Resource):
    def get(self):
        try:
            reports = Report.query.all()
            if reports:
                return jsonify(response([result.to_json() for result in reports]))
            else:
                return response('reports does`t exists', 400)
        except Exception as e:
            return response(f"{e}", 500)
