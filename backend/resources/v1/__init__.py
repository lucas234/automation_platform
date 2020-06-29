# coding=utf-8
# auther：Liul5
# date：9/16/2019 4:25 PM
# tools：PyCharm
# Python：3.7.3
from flask_restful import Api
from flask import Blueprint
from resources.v1.user import UserApi, UserToken, LoginResource, UserResource, UserListResource
from resources.v1.api import ApiResource, ApiListResource
from resources.v1.report import ReportResource, ReportListResource
from resources.v1.upload_download import UploadDownloadResource, ExcelUploadDownload
from resources.v1.tools import FakerDataResource


def register_resource_views(app):
    _api = Api(app)
    # _api.add_resource(UserApi, '/users', endpoint="add_user")
    # _api.add_resource(UserApi, '/users/<int:user_id>', endpoint="retrieve_user")
    # _api.add_resource(UserApi, '/users/<string:username>', endpoint="delete_user")
    # _api.add_resource(UserToken, '/refresh', endpoint='get_token')
    # _api.add_resource(UserToken, '/users/login', endpoint='login')

    # base wtf-form
    _api.add_resource(LoginResource, '/login', '/login/', endpoint='user login')
    _api.add_resource(LoginResource, '/token/refresh', endpoint='token refresh')
    _api.add_resource(UserResource, '/users/register', endpoint='register')
    _api.add_resource(UserResource, '/users/<int:user_id>', endpoint='retrieve or delete or update')
    _api.add_resource(UserListResource, '/users', endpoint='user list')
    _api.add_resource(ApiResource, '/apis/<int:api_id>', endpoint='apis by id')
    _api.add_resource(ApiResource, '/api', '/api/', endpoint='add apis')
    _api.add_resource(ApiListResource, '/apis', '/apis/', endpoint='apis list')

    # report
    _api.add_resource(ReportResource, '/reports/<int:report_id>', endpoint='report by id')
    # 兼容结尾带斜线"/"的
    _api.add_resource(ReportResource, "/report", "/report/", endpoint='add report')
    _api.add_resource(ReportListResource, '/reports', endpoint='reports list')
    # upload/download file
    _api.add_resource(ExcelUploadDownload, '/excel/upload', endpoint='upload excel')
    _api.add_resource(ExcelUploadDownload, '/excel/download', endpoint='download excel')
    _api.add_resource(UploadDownloadResource, '/download', endpoint='download file')

    # tools
    _api.add_resource(FakerDataResource, '/tools/info', endpoint='faker info')


def register_blueprints(app):
    # 注册版本
    """
    注册蓝图->v1版本
    """
    bp_v1 = Blueprint('v1', __name__)
    register_resource_views(bp_v1)
    app.register_blueprint(bp_v1, url_prefix='/v1')
